from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register', views.register, name = 'register'),
    path('login', views.loginUser, name = 'login'),
    path('add', views.addBook, name = 'add'),
    path('list', views.listInventory, name = 'listInventory'),
    path('editInventory', views.editInventory, name="editInventory"),
    path('deleteBook', views.deleteInventory, name="deleteInventory"),

]