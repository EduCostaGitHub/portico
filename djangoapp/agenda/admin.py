from django.contrib import admin

from agenda import models

# Register your models here.


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'phone', 'show'
    ordering = '-id',
    # list_filter = 'created_date',
    search_fields = 'id', 'first_name',
    list_per_page = 10
    list_max_show_all = 300
    list_editable = 'first_name', 'last_name', 'show'
    list_display_links = 'id',


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = '-id',
