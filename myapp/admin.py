from django.contrib import admin
from .models import Item, Order, Refund, User


class Admin(admin.ModelAdmin):
    pass

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Refund)