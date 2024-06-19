from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from store.models import Book, Inventory, Store, StoreBook
import requests

@login_required(login_url='/login')
def home(request):
    stores = Store.objects.filter(user=request.user)
    return render(request, 'index.html', {'stores': stores})

def logoutuser(request):
    logout(request)
    return redirect("/login")

@login_required(login_url='/login')
def addStore(request):
    if request.method == 'POST':
        store = Store(user=request.user, title=request.POST['title'])
        store.save()
        return redirect('/')
    return render(request, 'add_store.html')  

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    
    User = get_user_model()
    
    if request.method == 'POST':
        if request.POST['password'] != request.POST['confirm_password']:
            return render(request, 'register.html', {'err': 'Passwords do not match'})
        
        try:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            user.save()
            return redirect('/login')
        except Exception as e:
            return render(request, 'register.html', {'err': 'Username already taken'})
    
def loginUser(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/list')
            else:
                return redirect('/')
        else:
            return render(request, 'login.html', {'err': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required(login_url='/login')
def addBook(request):
    if not request.user.is_staff:
        return redirect('/')
    
    if request.method == 'GET':
        return render(request, 'add_book.html')
    
    if request.method == 'POST':
        r = requests.get(url=request.POST['link'])
        my_json = r.json()
        author = my_json['volumeInfo'].get('authors', ['Not Available'])[0]
        img = my_json['volumeInfo'].get('imageLinks', {}).get('thumbnail', "https://image.flaticon.com/icons/png/128/2748/2748558.png")
        
        if Book.objects.filter(link=request.POST['link']).exists():
            return render(request, 'add_book.html', {'err': 'Book already in the inventory cannot add it.'})
        
        book = Book(title=request.POST['title'], link=request.POST['link'], authors=author, image_link=img)
        book.save()
        
        inven = Inventory(book=book, count=request.POST['number'])
        inven.save()
        return redirect('/list')

@login_required(login_url='/login')
def listInventory(request):
    if not request.user.is_staff:
        return redirect('/')
    books = Inventory.objects.all()
    return render(request, 'list_inventory.html', {'books': books})

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
    inven.book.delete()
    return redirect('/list')

@login_required(login_url='/login')
def manageStore(request):
    if request.method == 'GET':
        store = Store.objects.get(id=request.GET['id'])
        books = StoreBook.objects.filter(store=store)
        return render(request, 'manage_store.html', {'books': books, 'store': store})
    
    if request.method == 'POST':
        storebook = StoreBook.objects.get(id=request.POST['id'])
        inven = Inventory.objects.get(book=storebook.book)
        inven.count += storebook.count
        storebook.delete()
        inven.save()
        return redirect(f'/managestore?id={storebook.store.id}')

@login_required(login_url='/login')
def storeBook(request):
    if request.method == "GET":
        inven = Inventory.objects.all()
        print(inven)
        return render(request, 'store_book.html', {'inven': inven, 'id': request.GET['id']})
    
    if request.method == "POST":
        inven = Inventory.objects.get(id=request.POST['id'])
        count = int(request.POST['count'])
        
        if inven.count >= count:
            store = Store.objects.get(id=request.POST['storeid'])
            storebook, created = StoreBook.objects.get_or_create(book=inven.book, store=store)
            
            if not created:
                storebook.count += count
            else:
                storebook.count = count
            
            storebook.save()
            inven.count -= count
            inven.save()
            return redirect(f'/managestore?id={request.POST["storeid"]}')
        
        return render(request, 'store_book.html', {'err': 'Not enough inventory', 'inven': Inventory.objects.all(), 'id': request.POST['storeid']})
