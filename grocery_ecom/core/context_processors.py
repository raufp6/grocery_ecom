from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,Cart,CartItem
from .cart import add_to_cart, remove_from_cart, get_cart

def default(request):
    # All active categories
    categories = Category.objects.filter(is_available=True)
    
    # Cart Items From Session
    try:
        cart_total = 0
        cart_data = request.session['cart_data_obj']
        for key,item in cart_data.items():
            cart_total += int(item['qty']) * float(item['price'])
    except:
        cart_data = None
        cart_total = 0
    # User Address
    try:
        address = Address.objects.get(user = request.user)
    except:
        address = None

    return {
        'categories':categories,
        'cart_data':cart_data,
        'cart_total':cart_total
    }