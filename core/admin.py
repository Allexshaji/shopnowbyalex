from django.contrib import admin
from seller.models import Product
from core.models import Notifications,User



admin.site.register(User)
admin.site.register(Product)