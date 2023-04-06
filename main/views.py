from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Q
import json
from django.middleware import csrf
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
    order, created = Order.objects.get_or_create(
        complete=False, customer=request.user)

    context = {"orderitem": orderitem, 'csrf_token': csrf.get_token(request)}
    return render(request, 'main/cart.html', context)


def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']
        product_id = data['id']

        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(
            complete=False, customer=request.user)
        orderitem, created = OrderItem.objects.get_or_create(
            product=product, order=order)

        if orderitem.quantity <= 0:
            orderitem.delete()

        if action == 'remove' and orderitem.quantity > 1:
            orderitem.quantity = orderitem.quantity - 1
        elif action == "add" and orderitem.quantity >= 0:
            orderitem.quantity = orderitem.quantity + 1
        orderitem.save()

        orders_total = ''
        order_total = 0
        for item in order.orderitem_set.all():
            items_total = item.quantity * item.product.price
            order_total += items_total
            orders_total = str(order_total)
        item_total = str(product.price * orderitem.quantity)

        response_data = {
            'qty': orderitem.quantity,
            'item_total': item_total,
            'orders_total': orders_total

        }

    elif request.method == 'GET':
        counts = OrderItem.objects.all().count()
        response_data = {
            'counts': counts,
        }

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


def cart_get_qty(request, pk):
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(
        complete=False, customer=request.user)
    orderitem = OrderItem.objects.filter(
        product=product, order=order).exists()

    orders_total = ''
    order_total = 0
    for item in order.orderitem_set.all():
        items_total = item.quantity * item.product.price
        order_total += items_total
        orders_total = str(order_total)

    if orderitem:
        cart_item = OrderItem.objects.get(product=product, order=order)
        response = {
            'qty': cart_item.quantity,
            'item_total': str(items_total),
            'orders_total': orders_total,

        }
    else:
        orderitem.delete()
        response = {
            'orders_total': orders_total,
        }

    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )


def get_qty(request, pk):

    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(
        complete=False, customer=request.user)
    orderitem = OrderItem.objects.filter(
        product=product, order=order).exists()

    if orderitem:
        cart_item = OrderItem.objects.get(order=order, product=product)
        response = {
            'qty': cart_item.quantity,
        }
    else:
        response = {
            'qty': 0
        }

    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )


def delete_item(request, pk):
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(
        complete=False, customer=request.user)
    order_item = OrderItem.objects.get(order=order, product=product)
    counts = OrderItem.objects.all().count()
    order_item.delete()
    orders_total = ''
    order_total = 0
    for item in order.orderitem_set.all():
        items_total = item.quantity * item.product.price
        order_total += items_total
        orders_total = str(order_total)
    return JsonResponse({'orders_total': orders_total, 'counts': counts})
