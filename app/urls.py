from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('purchase/', views.purchase),
    path('sales/', views.sales),
    path('purchaseprocess/', views.purchaseprocess),
    path('getitems/', views.getItems),
    path('getinventoryppi/', views.getInventoryPPI),
    path('salesprocess/', views.salesprocess),
    path('inventory/', views.inventory)
]