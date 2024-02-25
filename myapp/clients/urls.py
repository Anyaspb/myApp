from django.urls import path, include
from rest_framework import routers

from .views import OrderView, OrderPositionView, SupplierOrders, CartView, ClientView

urlpatterns = [
    # path('v1/', OrderView.as_view()),
    # path('v2/', OrderPositionView.as_view()),
    path('supplier/', SupplierOrders.as_view()),
    path('cart/', CartView.as_view()),
    path('client/', ClientView.as_view()),
]
