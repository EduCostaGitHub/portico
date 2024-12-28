from django.contrib import admin
from store.models import Product, ProductType, Requests, UserProfile, ItemRequest

# Register your models here.


class ProductTypeInLine(admin.TabularInline):
    model = ProductType
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = 'name', 'short_description', 'get_price_formated', 'get_promo_price_formated',
    inlines = [
        ProductTypeInLine,
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }


class RequestItemsInLine(admin.TabularInline):
    model = ItemRequest
    extra = 1


class RequestsAdmin(admin.ModelAdmin):
    inlines = [
        RequestItemsInLine,
    ]

# Register your models here.


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)
admin.site.register(UserProfile)
admin.site.register(Requests, RequestsAdmin)
admin.site.register(ItemRequest)
