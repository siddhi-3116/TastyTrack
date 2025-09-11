from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from .models import Product, Category, Order, OrderItem, ShippingAddress
from .utils import cartData
from .forms import ShippingAddressForm

def home(request):
    data = cartData(request)  # Get cart data
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'cartItems': data['cartItems'],  # Add cart items count
    }
    return render(request, 'store/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# ADD CUSTOM LOGOUT FUNCTION
def custom_logout(request):
    messages.success(request, 'You have been successfully logged out. Come back soon!')
    logout(request)
    return redirect('home')

def cart(request):
    data = cartData(request)
    
    context = {
        'items': data['items'],
        'order': data['order'],
        'cartItems': data['cartItems'],
    }
    return render(request, 'store/cart.html', context)

def add_to_cart(request, product_id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to add items to your cart!')
        return redirect('login')  # Redirect to login page
    
    try:
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        orderItem.quantity += 1
        orderItem.save()
        
        messages.success(request, f'{product.name} added to cart!')
        return redirect('cart')  # CHANGED FROM 'home' TO 'cart'
    except Product.DoesNotExist:
        messages.error(request, 'Product not found!')
        return redirect('home')

def remove_from_cart(request, product_id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to manage your cart!')
        return redirect('login')
    
    try:
        product = Product.objects.get(id=product_id)
        order = Order.objects.get(customer=request.user, complete=False)
        orderItem = OrderItem.objects.get(order=order, product=product)
        
        if orderItem.quantity > 1:
            orderItem.quantity -= 1
            orderItem.save()
        else:
            orderItem.delete()
        
        messages.info(request, f'{product.name} quantity updated!')
        return redirect('cart')
    except (Product.DoesNotExist, Order.DoesNotExist, OrderItem.DoesNotExist):
        messages.error(request, 'Item not found in your cart!')
        return redirect('cart')
    
def checkout(request):
    data = cartData(request)
    
    # Check if cart is empty
    if data['cartItems'] == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            # Save shipping address
            shipping_address = form.save(commit=False)
            shipping_address.customer = request.user
            shipping_address.order = data['order']
            shipping_address.save()
            
            # Mark order as complete
            order = data['order']
            order.complete = True
            order.save()
            
            messages.success(request, 'Order placed successfully! Thank you for your purchase.')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = ShippingAddressForm()
    
    context = {
        'items': data['items'],
        'order': data['order'],
        'cartItems': data['cartItems'],
        'form': form,
    }
    return render(request, 'store/checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    shipping_address = order.shipping_address
    
    context = {
        'order': order,
        'shipping_address': shipping_address,
        'cartItems': 0,  # Cart is empty after checkout
    }
    return render(request, 'store/order_confirmation.html', context)

def order_history(request):
    orders = Order.objects.filter(customer=request.user, complete=True).order_by('-date_ordered')
    
    context = {
        'orders': orders,
        'cartItems': cartData(request)['cartItems'],
    }
    return render(request, 'store/order_history.html', context)