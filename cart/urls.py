from django.urls import path
from .import views


urlpatterns = [
    path('', views.cart_list, name='cart_list'),
    path('cart_create/<int:computerId>', views.cart_create, name="cart_create"),
    path('remove_cart/<int:computerId>', views.remove_cart, name="remove_cart"),
    path('cart_delete/<int:caritemId>', views.cart_delete, name="cart_delete"),

    path('order_list', views.order_list, name='order_list'),
    path('order_create/<int:cartId>', views.order_create, name="order_create"),
    path('order_cancel/<int:orderId>', views.order_cancel, name="order_cancel"),
    path('order_complete/<int:orderId>', views.order_complete, name="order_complete")
]