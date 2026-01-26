from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def stockIn(request):
    return render(request, 'StockAdd.html')

def stockOut(request):
    return render(request, 'Stockout.html')

def viewInventory(request):
    return render(request, 'ViewInventory.html')
def history(request):
    return render(request, 'history.html')


# Create your views here.
