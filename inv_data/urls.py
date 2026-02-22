from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('stockIn', views.stockIn, name='stockIn'),
    path('viewInventory', views.viewInventory, name='viewInventory'),
    path('history', views.history, name='history'),
]