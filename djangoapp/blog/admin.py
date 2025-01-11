from django.contrib import admin
from django.http import HttpRequest
from blog.models import MenuLink, SiteSetup
from blog.models import Category, Page, Post, Tag
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


# Register your models here.
# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id' , 'text' , 'url_or_path',
#     list_display_links = 'id' , 'text' , 'url_or_path',
#     search_fields = 'id' , 'text' , 'url_or_path',

class MenuLinkInLine(admin.TabularInline):
    model = MenuLink
    extra = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description'
    inlines = MenuLinkInLine,

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not SiteSetup.objects.exists()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('name',),
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('name',),
    }


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'content',
    list_per_page = 50
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',),
    }


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published', 'created_by'
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'excerpt', 'content',
    list_per_page = 50
    list_filter = 'category', 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    readonly_fields = (
        'created_at',
        'updated_at',
        'updated_by',
        'created_by',
        'link',
    )
    prepopulated_fields = {
        "slug": ('title',),
    }
    autocomplete_fields = 'tags', 'category'

    def link(self, obj):
        if not obj.pk:
            return '-'

        post_url = obj.get_absolute_url()
        safe_link = mark_safe(f'<a target="_blank" href="{post_url}">Post</a>')

        return safe_link

    def save_model(self, request, obj, form, change) -> None:
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user

        obj.save()
