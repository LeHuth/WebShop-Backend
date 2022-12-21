from django.db import models
import Members.models
from Members.models import Member
from Products.models import Product


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
