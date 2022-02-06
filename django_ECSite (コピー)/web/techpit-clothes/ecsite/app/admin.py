from django.contrib import admin
from .models import Product, Cart, line_items


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(line_items)
