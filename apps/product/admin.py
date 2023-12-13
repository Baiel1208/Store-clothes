from django.contrib import admin

from apps.product import models as m

# Register your models here.
admin.site.register(m.Product)
admin.site.register(m.ProductCategory)