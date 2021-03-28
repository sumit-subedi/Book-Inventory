from django.contrib import admin
from .models import Book, Inventory, Store, storeBooks

admin.site.register(Book)
admin.site.register(Inventory)
admin.site.register(Store)
admin.site.register(storeBooks)