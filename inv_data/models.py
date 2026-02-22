from django.db import models


# =========================
# CATEGORY MODEL
# =========================
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name
    
# =========================
# STORES MODEL
# =========================

class Store(models.Model):
    store_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.store_name


# =========================
# PRODUCT MODEL
# =========================
class Product(models.Model):
    product_code = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("product_code", "product_name", "category")

    def __str__(self):
        return f"{self.product_code} - {self.product_name}"
    

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.supplier_name

class ImportedFor(models.Model):
    imported_for = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.imported_for

# =========================
# STOCK TRANSACTION MODEL
# =========================
class StockTransaction(models.Model):

    status = models.CharField(max_length=30)
    remark = models.TextField(blank=True, null=True)
    received_date = models.DateField()
    imported_for = models.ForeignKey(
        ImportedFor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.status} - {self.received_date}"


# =========================
# STOCK TRANSACTION ITEM MODEL
# =========================
class StockTransactionItem(models.Model):
    transaction = models.ForeignKey(
        StockTransaction,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    market_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    total_market = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    from_location = models.CharField(max_length=100, blank=True, null=True)
    to_location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'store')

    def __str__(self):
        return f"{self.product} - {self.store} ({self.quantity})"
