from decimal import Decimal
from django.shortcuts import render, redirect
from django.db.models import Q
from inv_data.models import (
    Category, Store, Supplier, ImportedFor,
    Product, StockTransaction, StockTransactionItem, Inventory
)
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField
from django.http import HttpResponseBadRequest

def index(request):
    product = Product.objects.all()
    inventory = Inventory.objects.select_related("product")

    count = 0
    total_mp = 0

    for item in inventory:
        count += item.quantity

        last_item = item.product.stocktransactionitem_set.order_by("-id").first()

        if last_item and last_item.market_price:
            total_mp += item.quantity * last_item.market_price
        else:
            total_mp += 0

    total_mp_twd = total_mp / Decimal("4.58")


    return render(request, 'index.html', {
        'product': product,
        'count': count,
        'total_mp': total_mp,
        'total_mp_twd': total_mp_twd
    })

# -----------------------
# STOCK IN VIEW
# -----------------------

# inv_data/views.py


def stockIn(request):
    categories = Category.objects.all()
    stores = Store.objects.all()
    suppliers = Supplier.objects.all()
    imported_for = ImportedFor.objects.all()

    if request.method == "POST":
        force_create = request.POST.get("force_create") == "true"

        # ---------------- GET FORM DATA ----------------
        status = request.POST.get("status")
        code = request.POST.get("code")
        category_name = request.POST.get("category")
        product_name = request.POST.get("product_name")
        quantity = int(request.POST.get("quantity") or 0)
        market_price = request.POST.get("market_price")
        total_market = request.POST.get("total_market")
        cost_price = request.POST.get("cost_price")
        total_cost = request.POST.get("total_cost")
        received_date = request.POST.get("received_date")
        remark = request.POST.get("remark")

        supplier_name = request.POST.get("supplier")
        imported_for_name = request.POST.get("imported_for")
        from_location = request.POST.get("from_location")
        to_location = request.POST.get("to_location")

        # ---------------- OBJECTS ----------------
        category = Category.objects.get(category_name=category_name)

        supplier = Supplier.objects.filter(supplier_name=supplier_name).first() if supplier_name else None
        imported_for_obj = ImportedFor.objects.filter(imported_for=imported_for_name).first() if imported_for_name else None
        from_store = Store.objects.filter(store_name=from_location).first() if from_location else None
        to_store = Store.objects.filter(store_name=to_location).first() if to_location else None

        # ---------------- PRODUCT ----------------
        exact_match = Product.objects.filter(
            product_code=code,
            product_name=product_name,
            category=category
        ).first()

        partial_match = Product.objects.filter(
            product_code=code,
            category=category
        ).exclude(product_name=product_name)

        if partial_match.exists() and not exact_match and not force_create:
            return render(request, "StockAdd.html", {
                "warning": partial_match,
                "categories": categories,
                "stores": stores,
                "suppliers": suppliers,
                "imported_for": imported_for,
                "form_data": request.POST,
            })

        if exact_match:
            product = exact_match
        else:
            # create NEW row (no update of old rows)
            product = Product.objects.create(
                product_code=code,
                product_name=product_name,
                category=category
            )

        # ---------------- TRANSACTION ----------------
        transaction_obj = StockTransaction.objects.create(
            status=status,
            remark=remark,
            received_date=received_date,
            supplier=supplier,
            imported_for=imported_for_obj
        )
        last_item = StockTransactionItem.objects.filter(
            product=product
        ).order_by("-id").first()

        prev_cost = last_item.cost_price if last_item else None
        prev_market = last_item.market_price if last_item else None


        StockTransactionItem.objects.create(
            transaction=transaction_obj,
            product=product,
            quantity=quantity,
            cost_price=cost_price or prev_cost,
            market_price=market_price or prev_market,
            total_cost=total_cost or None,
            total_market=total_market or None,
            from_location=from_location or None,
            to_location=to_location or None,
        )


        # ---------------- INVENTORY UPDATE ----------------
        if status == "now_stock":
            inv, _ = Inventory.objects.get_or_create(product=product, store=to_store, defaults={"quantity": 0})
            inv.quantity += quantity
            inv.save()
            
        elif status == "sold_out":
            if not from_store:
                return HttpResponseBadRequest("From store is required for sold out")

            try:
                inv = Inventory.objects.get(product=product, store=from_store)
            except Inventory.DoesNotExist:
                return HttpResponseBadRequest("No such product in stock")

            if inv.quantity < quantity:
                return HttpResponseBadRequest("Not enough stock to sell")

            # ✅ Just reduce quantity — DO NOT touch prices
            inv.quantity -= quantity
            inv.save()

            # ✅ IMPORTANT: copy existing prices into the transaction
            last_item = StockTransactionItem.objects.filter(
                product=product
            ).order_by("-id").first()

            if last_item:
                # update the just-created transaction item with existing prices
                StockTransactionItem.objects.filter(
                    transaction=transaction_obj,
                    product=product
                ).update(
                    cost_price=last_item.cost_price,
                    market_price=last_item.market_price,
                    total_cost=(last_item.cost_price or 0) * quantity if last_item.cost_price else None,
                    total_market=(last_item.market_price or 0) * quantity if last_item.market_price else None,
                )



        elif status == "stock_transfer":
            from_inv, _ = Inventory.objects.get_or_create(product=product, store=from_store, defaults={"quantity": 0})
            to_inv, _ = Inventory.objects.get_or_create(product=product, store=to_store, defaults={"quantity": 0})

            from_inv.quantity -= quantity
            to_inv.quantity += quantity

            from_inv.save()
            to_inv.save()

        return redirect("stockIn")

    # ---------------- GET REQUEST ----------------
    return render(request, "StockAdd.html", {
        "categories": categories,
        "stores": stores,
        "suppliers": suppliers,
        "imported_for": imported_for,
    })


# -----------------------
# STOCK OUT VIEW
# -----------------------
def stockOut(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'Stockout.html', context)

# -----------------------
# VIEW INVENTORY
# -----------------------
def viewInventory(request):
    latest_item = StockTransactionItem.objects.filter(
        product=OuterRef("product")
    ).order_by("-id")

    inventory = Inventory.objects.select_related(
        "product",
        "product__category",
        "store"
    ).annotate(
        market_price=Subquery(latest_item.values("market_price")[:1]),
        cost_price=Subquery(latest_item.values("cost_price")[:1]),
    ).annotate(
        total_market=ExpressionWrapper(
            F("quantity") * F("market_price"),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        ),
        total_cost=ExpressionWrapper(
            F("quantity") * F("cost_price"),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        ),
    )

    return render(request, "ViewInventory.html", {
        "inventory": inventory
    })



# -----------------------
# HISTOR
# -----------------------
def history(request):
    transactions = StockTransactionItem.objects.select_related(
        "product",
        "product__category",
        "transaction",
        "transaction__supplier",
        "transaction__imported_for",
    ).order_by("-transaction__received_date")

    return render(request, "history.html", {
        "transactions": transactions
    })
