from django.shortcuts import get_object_or_404
from .models import Cart,CartItem,Product

def get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    cart = None
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
    if not cart:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart

def add_to_cart(request, product_id, quantity=1):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
        item.save()

def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()

def get_cart(request):
    cart = get_or_create_cart(request)
    return cart
