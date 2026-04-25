from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('stockIn', views.stockIn, name='stockIn'),
    path('viewInventory', views.viewInventory, name='viewInventory'),
    path('history', views.history, name='history'),
    path('edit-inventory/<int:id>/', views.edit_inventory, name='edit_inventory'),
    path('delete-inventory/<int:id>/', views.delete_inventory, name='delete_inventory'),
]