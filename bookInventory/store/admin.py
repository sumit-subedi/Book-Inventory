from django.contrib import admin
from .models import Book, Inventory

admin.site.register(Book)
admin.site.register(Inventory)