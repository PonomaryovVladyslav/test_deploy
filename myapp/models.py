from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(blank=False)
    funds = models.FloatField(default=1000)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    amount_available = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name='item')
    create_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=1)

    @property
    def count_total_price(self):
        return self.item.price * self.amount


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    crate_date = models.DateTimeField(auto_now_add=True)






