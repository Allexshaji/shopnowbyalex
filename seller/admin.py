from django.contrib import admin
from .models import Category, SubCategory, ProductImage
from seller.models import SellerProfile,VerifiedDoc

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductImage)
admin.site.register(SellerProfile)
admin.site.register(VerifiedDoc)
