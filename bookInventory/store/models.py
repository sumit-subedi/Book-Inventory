from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    Title = models.CharField(max_length=100)
    Link = models.CharField(max_length=200)
    Authors = models.CharField(max_length=200)
    imageLink = models.CharField(max_length=100)

    def __str__(self):
      return self.Title

class Inventory(models.Model):
  Book = models.OneToOneField(Book, on_delete=models.CASCADE)
  count = models.IntegerField(default=1)

  def __str__(self):
    return str(self.Book)

class Store(models.Model):
  user = models.ForeignKey(User, related_name='ownedby', on_delete=models.CASCADE)
  Book = models.OneToOneField(Book, on_delete=models.CASCADE)
  count = models.IntegerField(default=1)