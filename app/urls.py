from django.urls import path
from .views import *
urlpatterns = [

    # Pages 
    path('', home, name="home"),
    path('product-details/<uuid:pk>/', product_details, name="product-details"),
    path('update-cart/', update_cart, name="update-cart"),
    path('cart/', cart, name='cart'),
    path('about/' ,about,name='about'),


    # FOR THE ADD TO CART 
    path("get-qty/",get_qty, name="get-qty" ),
    path("cart-get-qty/",cart_get_qty, name="cart-get-qty" ),
    path("get-total-item/",get_total_item, name="get-total-item"),

]