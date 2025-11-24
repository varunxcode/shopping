from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet, OrderItemViewSet, product_list, product_detail, add_to_cart, cart_detail, checkout, register, remove_from_cart, order_history

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('register/', register, name='register'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('orders/', order_history, name='order_history'),
]
