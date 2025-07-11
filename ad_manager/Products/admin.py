from django.contrib import admin
from .models import Product, Category, Brand, Dimensions, RealDimension, ManufacturerCode, ProductSpecifications


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Dimensions)
admin.site.register(RealDimension)
admin.site.register(ManufacturerCode)
admin.site.register(ProductSpecifications)