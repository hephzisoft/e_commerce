from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
import json

from .models import Product, Order, OrderItem
from user.models import User


def home(request):
    q = request.GET.get('q')
    if q:
        products = Product.objects.filter(Q(name__icontains=q))
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'main/home.html', context)


def product_details(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product
    }
    return render(request, 'main/products-details.html', context)


def cart(request):
    orderitem = OrderItem.objects.all()
    context = {
        'orderitem': orderitem
    }
    return render(request, 'main/cart.html',)


def update_cart(request):
    if request.method == 'POST':
        data = json.dumps(request.body)
        action = data['action']
        product_id = data['id']
        print(action)
        print(product_id)
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(
            customer=request.user, complete=False)
        orderitem = OrderItem.objects.get_or_create(
            product=product, order=order)

        if action == "add" and orderitem.quantity >= 0:
            orderitem.quantity = orderitem.quantity + 1
        elif action == "add" and orderitem.quantity > 0:
            orderitem.quantity = orderitem.quantity - 1

            pass
        context = {
            'message': 'Item updated',
            'qty': orderitem.quantity
        }
        return JsonResponse(context)

    elif request.method == "GET":
        context ={
            'qty': orderitem.quantity
        }
