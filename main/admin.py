from django.contrib import admin
from .models import Product, Order, OrderItem, Checkout


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("quantity",)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display=("id")
