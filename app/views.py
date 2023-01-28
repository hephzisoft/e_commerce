from django.shortcuts import render
from .models import *
import json
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.http import  HttpResponse


def home(request):
    q = request.GET.get('q') 
    if q:
        products = Product.objects.filter(Q(name__icontains=q))
    else:
        products = Product.objects.all()
  

    context = {

        'products':products
    }
    return render(request, 'app/home.html', context)


def product_details(request, pk):
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(
        complete=False, customer=request.user)

    context = {
        'product': product,

    }
    return render(request, 'app/products-details.html', context)


def update_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    action = data['action']

    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        complete=False, customer=request.user)
    orderitem, created = OrderItem.objects.get_or_create(
        product=product, order=order)
    if action == "add":
        if orderitem.quantity >= 0:
            orderitem.quantity = orderitem.quantity + 1

    elif action == "remove":
        if orderitem.quantity > 0:
            orderitem.quantity = orderitem.quantity - 1

    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()

    response_data = {
        'qty': orderitem.quantity
    }
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


def get_qty(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        complete=False, customer=request.user)
    orderitem, created = OrderItem.objects.get_or_create(
        product=product, order=order)

    response = {
        'qty': orderitem.quantity
    }
    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )


def cart_get_qty(request):
    data = json.loads(request.body)
    product_id = data['id']
    print(product_id)
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        complete=False, customer=request.user)
    orderitem, created = OrderItem.objects.get_or_create(
        product=product, order=order)

    response = {
        'qty': orderitem.quantity,
    }
    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )

@csrf_protect
def get_total_item(request):
    counts = OrderItem.objects.all().count()
    print(counts)
    response = {
        "counts": counts
    }
    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )


def cart(request):
    orderitem = OrderItem.objects.all()

    context = {"orderitem": orderitem}
    return render(request, 'app/cart.html', context)


def about(request):
    return render (request, 'app/about.html')