
from django.shortcuts import render,redirect
# from django.http import HttpResponse
from django.contrib.auth.models import User
import re, json, requests
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from store.models import Book, Inventory

@login_required(login_url='/login')

def home(request):
  book = "Hamlet"
  book_url="https://www.googleapis.com/books/v1/volumes?q={}&maxResults=5&startIndex=0".format(book)
  print(book_url)
  r = requests.get(url=book_url)
  my_json= r.json()
  books = []
  for i in my_json["items"]:
    
    books.append(i['volumeInfo']['title'])
  
  
  return render(request,'index.html', {'items':books})

def register(request):
  if request.method == 'GET':
    return render(request, 'register.html')
  User = get_user_model()
  # user = User.objects.create_user(username = 'john2', password = 'john123')
  # user.save()
  # print(user.is_staff)
  if request.method == 'POST':
    print(request.POST)
    if request.POST['password'] != request.POST['confirm_password']:
      
      return render (request, 'register.html', {'err':'No matching password'})
    try:
      user = User.objects.create_user(username = request.POST['username'], password = request.POST['password'])
      user.save()
      return redirect('/login')
    
    except Exception as e:
      return render (request, 'register.html', {'err':'Username already taken'})
  
def loginUser(request):

  if request.method == "POST":
    
    print('here')
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
      print(request)
      login(request, user)
      if user.is_staff:
        return redirect('/list')
      else:
        return redirect('/')
    else:
      print('here')
      return render(request, 'login.html', {'err':'NO such Username or Password Check Again.'})
  
  else:
    return render (request, 'login.html')

@login_required(login_url='/login')
def addBook(request):
  if not request.user.is_staff:
    return redirect('/')
  if request.method =='GET':
    return render(request, 'add.html')

  if request.method == 'POST':

    r = requests.get(url=request.POST['link'])
    my_json= r.json()
    if 'authors' in my_json['volumeInfo']:
      author =  my_json['volumeInfo']['authors']
    else:
      author = "Not Available"

    if 'imageLinks' in my_json['volumeInfo']:
      img = my_json['volumeInfo']['imageLinks']['thumbnail']
    else:
      img = "https://image.flaticon.com/icons/png/128/2748/2748558.png"
    
    
    # Check if book is already on Inventory if yes then send error
    if Book.objects.filter(Link = request.POST['link']):
      return render(request, 'add.html', {'err':'Book already in the inventory cannot add it.'})
    
    # Adding book to the inventory
    # First Creating a Book object
    book = Book(Title=request.POST['title'], Link=request.POST['link'], Authors = author, imageLink=img)
    book.save()

    # Adding that book to the inventory
    inven = Inventory(Book = book, count=request.POST['number'])
    inven.save()
    return render(request, 'add.html')

@login_required(login_url='/login')
def listInventory(request):
  if not request.user.is_staff:
    return redirect('/')
  books = Inventory.objects.all()
  
  
  return render(request, 'list.html',{'books':books})

@login_required(login_url='/login')
def editInventory(request):
  if not request.user.is_staff:
    return redirect('/')
  
  inven = Inventory.objects.get(id=request.POST['id'])
  inven.count = request.POST['quantity']
  inven.save()
  return redirect('/list')

@login_required(login_url='/login')
def deleteInventory(request):
  if not request.user.is_staff:
    return redirect('/')
  inven = Inventory.objects.get(id=request.POST['id'])
  inven.Book.delete()
  return redirect('/list')