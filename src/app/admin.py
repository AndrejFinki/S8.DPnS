from django.contrib import admin
from .models import Image, Word


# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'algorithm', 'is_processed')
    search_fields = ('name',)
    list_filter = ('algorithm',)
    ordering = ('-id',)
    list_per_page = 10
    list_select_related = True
    fieldsets = (
        (None, {
            'fields': ('name', 'algorithm', 'is_processed')
        }),
        ('Image Details', {
            'fields': ('image', 'is_processed'),
        }),
    )
    
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'image')
    search_fields = ('word',)
    list_filter = ('image',)
    ordering = ('-id',)
    list_per_page = 10
    list_select_related = True
    fieldsets = (
        (None, {
            'fields': ('word', 'image')
        }),
    )