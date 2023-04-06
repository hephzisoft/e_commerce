from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import MinValueValidator
from user.models import User




class Product(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=7,   decimal_places=2, validators=[MinValueValidator(0)])
    image = models.URLField(blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    complete = models.BooleanField(default=False, blank=False, null=True)
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    transaction_id = models.CharField(max_length=30, blank=True, unique=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    quantity = models.IntegerField(default=0, null=True, )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)


class Checkout(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_created=True)
    zipcode = models.CharField(max_length=200, null=True)
