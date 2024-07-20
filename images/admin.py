# admin.py
from django.contrib import admin
from .models import Image, Category

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title']
    filter_horizontal = ('categories',)

admin.site.register(Category)
