from django.shortcuts import render, redirect, get_object_or_404
from computers.models import Computer, Wishlist, WishlistItem
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile
from django.db.models import Q

# Create your views here.
def index(request):
    query = request.GET.get('q', '')
    if query:
        computers = Computer.objects.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(processor__icontains=query) |
            Q(storage__icontains=query) |
            Q(price__icontains=query)
        )
    else:
        computers = Computer.objects.all()
    
    for computer in computers:
        if not request.user.is_authenticated:
            computer.wishlisted = False
        else:
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            wishlisted = WishlistItem.objects.filter(wishlist=wishlist, computer=computer).exists()
            computer.wishlisted = wishlisted
    return render(request, 'index.html', {'computers':computers})

def computer_detail(request, id):
    computer = Computer.objects.get(id=id)
    custom_specs = {}
    print('computer.custom_specs',len(computer.custom_specs))
    if len(computer.custom_specs) > 0:
        custom_ss=computer.custom_specs.split(';')
        print('custom_ss',len(custom_ss))
        for ss in custom_ss:
            custom_specs[ss.split(':')[0]] = ss.split(':')[1]
    wishlisted = False
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlisted = WishlistItem.objects.filter(wishlist=wishlist, computer=computer).exists()
    return render(request, 'details.html', {'computer':computer, 'custom_specs':custom_specs, 'wishlisted':wishlisted})

def wishlist_toggle(request, computerId):
    if not request.user.is_authenticated:
        return redirect('login')
    computer = get_object_or_404(Computer, id=computerId)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    try:
        wishlist_item = WishlistItem.objects.get(wishlist=wishlist, computer=computer)
        wishlist_item.delete()
    except WishlistItem.DoesNotExist:
        WishlistItem.objects.create(wishlist=wishlist, computer=computer)
    return redirect('details', computer.id)



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        profile_photo = request.FILES.get('profile_photo')
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        user = User.objects.create_user(username=username, password=password, email=email)
        if profile_photo:
            Profile.objects.create(user=user, profile_photo=profile_photo)
        auth_login(request, user)
        return redirect('index')

    return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')  
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('index')