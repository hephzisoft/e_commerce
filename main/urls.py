from django.urls import path
from .views import home,cart,product_details,update_cart

urlpatterns=[
    path("",  home, name="home"),
    path("product-details/<uuid:pk>/",product_details, name="product-details" ),
    path("cart/", cart, name="cart"),

    # Add to cart  functionality 
    path("update-cart", update_cart, name="update-cart"),
]