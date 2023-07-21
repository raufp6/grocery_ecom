from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,Cart,CartItem
from .cart import add_to_cart, remove_from_cart, get_cart
from core.views import _session_id,merge_carts

def default(request):
    # All active categories
    categories = Category.objects.filter(is_available=True)
    
    total_amount = 0
    merge_carts(request)  # Merge the session cart with the user's cart
    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                product_item = item.product.items.get(is_default=True)
                total_amount =+ product_item.discount_price
                total_mrp_amount =+ product_item.price

            # total_amount = sum(item.product.items.discount_price * item.qty for item in cart_items)
            # total_mrp_amount = sum(item.product.price * item.qty for item in cart_items)
        except:
            cart = None
            cart_items = None
            total_amount = 0
            total_mrp_amount = 0
    else:
        try:
            cart_items = CartItem.objects.filter(session_id = _session_id(request))
            total_amount = sum(item.product.discount_price * item.qty for item in cart_items)
            total_mrp_amount = sum(item.product.price * item.qty for item in cart_items)
        except:
            cart = None
            cart_items = None
            total_mrp_amount = 0
            total_amount = 0
    # print(cart_items)


    # quantity = 0
    # count = 0
    # cart_total = 0
    # if request.user.is_authenticated:
    #     try:
    #         cart = Cart.objects.get(user=request.user)
    #         cart_items = CartItem.objects.filter(cart=cart)
    #     except:
    #         cart = None
    #         cart_items = None
    # else:
    #     try:
    #         cart = Cart.objects.get(session_id = _session_id(request))
    #         cart_items = CartItem.objects.filter(cart=cart)
    #     except:
    #         cart = None
    #         cart_items = None
    # if cart_items is not None:        
    #     for cart_item in cart_items:
    #         cart_total += cart_item.sub_total()
    #         quantity += cart_item.qty
    #         count += 1
    
    # print(count)
    # print(_session_id(request))
    
    # Cart Items From Session
    # try:
    #     cart_total = 0
    #     cart_data = request.session['cart_data_obj']
    #     for key,item in cart_data.items():
    #         cart_total += int(item['qty']) * float(item['price'])
    # except:
    #     cart_data = None
    #     cart_total = 0
    # User Address
    try:
        address = Address.objects.get(user = request.user)
    except:
        address = None

    return {
        'categories':categories,
        'cart_data':cart_items,
        'cart_total':total_amount,
        'total_mrp_amount':total_mrp_amount
    }