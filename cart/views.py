from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart, CartItem, Order
from computers.models import Computer
from django.utils import timezone
from datetime import timedelta

# Create your views here.

def cart_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart, status='noOrderPlaced').order_by('-created_at')
    for item in cart_items:
        item.total_price = item.price * item.quantity
    return render(request, 'cart.html', {'cart_items':cart_items})

def cart_create(request, computerId):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    computer = get_object_or_404(Computer, id=computerId)
    if computer.stock >= 1:
        cartitem, created = CartItem.objects.get_or_create(cart=cart, computer=computer, defaults={'quantity': 1, 'price': computer.price})
        
        if not created:
            cartitem.quantity += 1
            cartitem.save()
        computer.stock-=1
        computer.save()
    return redirect('cart_list')

def remove_cart(request, computerId):
    cart = Cart.objects.get(user=request.user)
    computer = Computer.objects.get(id=computerId)
    cartitem=CartItem.objects.get(cart=cart, computer=computer)
    computer.stock+=1
    computer.save()
    if cartitem.quantity == 1:
        cartitem.delete()
    else:
        cartitem.quantity -= 1
        cartitem.save()
    return redirect('cart_list')

def cart_delete(request, caritemId):
    cartitem = CartItem.objects.get(id =caritemId)
    cartitem.delete()
    return redirect('cart_list')


def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    now = timezone.now()
    for order in orders:
        if order.status == 'Pending' and now >= order.created_at + timedelta(minutes=5):
            order.status = 'Shipped'
            order.save()
    return render(request, 'order.html', {'orders':orders})

def order_create(request, cartId):
    cart = CartItem.objects.get(id=cartId)
    total_price = cart.price * cart.quantity
    if request.method=='POST':
        
        order = Order(
            user = request.user,
            computer = cart.computer,
            price = total_price,
            quantity = cart.quantity
        )
        print(order)
        order.save()
        cart.status='orderPlaced'
        cart.save()
        return redirect('order_list')
    return render(request, 'payment.html', {'total_price':total_price})

def order_cancel(request, orderId):
    order = Order.objects.get(id=orderId)
    computer = order.computer
    computer.stock += order.quantity
    computer.save()
    order.status = 'Cancelled'
    order.delivery_date = timezone.now().date()
    order.save()
    return redirect('order_list')

def order_complete(request, orderId):
    order = Order.objects.get(id=orderId)
    order.status = 'Completed'
    order.delivery_date = timezone.now().date()
    order.save()
    return redirect('order_list')
