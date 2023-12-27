from django.contrib import admin

from apps.product import models as m

# Register your models here.
# admin.site.register(m.Product)
admin.site.register(m.ProductCategory)


@admin.register(m.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'image', 'category') # ('price', 'quantity') в один ряд стоит
    # readonly_fields = ('category', )   # для чтение
    search_fields = ('name', )
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = m.Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp', )
    extra = 0