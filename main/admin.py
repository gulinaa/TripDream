from django.contrib import admin
from main.models import DestinationImage, Category, Destination


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage


class DestinationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = ['id', 'name']
    list_filter = ['category']
    search_fields = ['name', 'description']
    inlines = [DestinationImageInline]


admin.site.register(Category)
admin.site.register(Destination, DestinationAdmin)
