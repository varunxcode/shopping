from rest_framework import viewsets
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem

# Existing: product_list, product_detail

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/cart_detail.html', {'cart_items': items, 'total': total})

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    if request.method == "POST":
        # First: Check stock for all items
        for item in items:
            if item.quantity > item.product.stock:
                return render(request, 'shop/checkout.html', {
                    'cart_items': items,
                    'total': sum(i.product.price * i.quantity for i in items),
                    'error': f"Sorry, only {item.product.stock} left for {item.product.title}."
                })
        # Then: Proceed to create order if stock is available
        order = Order.objects.create(user=request.user)
        for item in items:
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity, price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
        items.delete()  # Clear the cart
        return render(request, 'shop/checkout_success.html', {'order': order})
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/checkout.html', {'cart_items': items, 'total': total})


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

@login_required
def remove_from_cart(request, pk):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=pk)
    item.delete()
    return redirect('cart_detail')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})

from .models import Product, Category

def product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })

def product_list(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q')
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    if query:
        products = products.filter(title__icontains=query)  # Add more fields as needed
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'query': query or '',
    })
