from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,Cart,CartItem
from .cart import add_to_cart, remove_from_cart, get_cart
from core.views import _session_id,merge_carts

def default(request):
    # All active categories
    categories = Category.objects.filter(is_available=True)
    total_mrp_amount = 0
    total_amount = 0
    # merge_carts(request)  # Merge the session cart with the user's cart
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user_id = request.user)
            cart_items = CartItem.objects.filter(cart = cart)
            total_amount = sum(item.product.discount_price * item.qty for item in cart_items)
            total_mrp_amount = sum(item.product.price * item.qty for item in cart_items)
        except:
            cart = None
            cart_items = None
            total_amount = 0
            total_mrp_amount = 0
    else:
        try:
            cart = Cart.objects.get(cart_id = _session_id(request))
            cart_items = CartItem.objects.filter(cart = cart)
            total_amount = sum(item.product.discount_price * item.qty for item in cart_items)
            total_mrp_amount = sum(item.product.price * item.qty for item in cart_items)
        except:
            cart = None
            cart_items = None
            total_mrp_amount = 0
            total_amount = 0

    try:
        address = Address.objects.get(user = request.user)
    except:
        address = None
    final_amount = float(total_amount)
    discount_amount = 0
    if 'discount_amount' in request.session and request.session['discount_amount']>0:
        total_amount = float(total_amount)
        final_amount -= float(request.session['discount_amount'])
        discount_amount = request.session['discount_amount']
    
    saved_amount = float(total_mrp_amount) - float(final_amount)
    return {
        'categories':categories,
        'cart_data':cart_items,
        'cart_total':total_amount,
        'discount_amount':discount_amount,
        'final_amount':final_amount,
        'total_mrp_amount':total_mrp_amount,
        'saved_amount':saved_amount
    }