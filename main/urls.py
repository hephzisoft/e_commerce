from django.urls import path
from .views import home, cart, product_details, update_cart, delete_item, cart_get_qty,get_qty

urlpatterns = [
    path("",  home, name="home"),
    path("product-details/<uuid:pk>/", product_details, name="product-details"),
    path("cart/", cart, name="cart"),

    # Add to cart  functionality
    path("get-qty/<uuid:pk>/", get_qty, name="get-qty"),
    path('update-cart/', update_cart, name="update-cart"),
    path('delete-item/<uuid:pk>/', delete_item, name="delete-item"),
    path("cart-get-qty/<uuid:pk>/", cart_get_qty, name="cart-get-qty"),]
