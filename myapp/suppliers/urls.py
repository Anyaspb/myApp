from django.urls import path, include
from rest_framework import routers

from .views import CategoryView, SupplierView, ProductView, SupplierState, PriceUpdate, CatalogView, ProductImport

router = routers.DefaultRouter()
router.register(r'products', ProductView)
router.register(r'category', CategoryView)
router.register(r'supplier', SupplierView)


urlpatterns = [
    path('', CatalogView.as_view()),
    path('', include(router.urls)),
    path('supplier-state/', SupplierState.as_view()),
    path('price-update/', PriceUpdate.as_view()),
    path('product-import/', ProductImport.as_view())
]
