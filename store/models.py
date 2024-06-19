from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    image_link = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class Inventory(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return str(self.book)

class Store(models.Model):
    user = models.ForeignKey(User, related_name='stores', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class StoreBook(models.Model):
    store = models.ForeignKey(Store, related_name='store_books', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='store_books', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return str(self.book)
