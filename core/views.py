from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from core.models import Category, Vendor, Brand, Product, ProductItem, ProductImages, CartOrder, CartOrderItems, ProductReview, WhishList, Countrty, State, City, Address, Cart, CartItem, OrderAddress, Variation, Coupon, Wallet, WalletTransaction
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from cart.cart import Cart
from django.db.models import Q
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from django.core import serializers


def index(request):
    products = Product.objects.filter(
        featured=True, product_status="published")

    context = {
        'products': products
    }
    return render(request, 'core/index.html', context)


def product_list(request):
    products = Product.objects.filter(product_status="published")

    context = {
        'products': products
    }
    return render(request, 'core/products.html', context)


def search(request):
    products = Product.objects.filter(product_status="published")
    query = request.GET['query']
    c = request.GET['c']
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    if query:
        products = Product.objects.filter(
            Q(description__icontains=query) | Q(title__icontains=query))
    if request.GET['c']:
        products = Product.objects.filter(category=request.GET['c'])

    if request.GET['min_price'] and request.GET['max_price']:
        products = Product.objects.filter(
            discount_price__range=(min_price, max_price))
    context = {
        'products': products,
        'query': query,
        'max_price': max_price,
        'min_price': min_price,
        'c': c

    }
    return render(request, 'core/products.html', context)


def category_list(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'core/categories.html', context)

# Prodcut Detail


def product_detail(request, pid, slug):
    product = Product.objects.get(pid=pid)
    p_images = product.p_images.all()

    context = {
        'product': product,
        'p_images': p_images,
    }
    return render(request, 'core/product-details.html', context)


def get_variation_price(request):
    if request.GET['id']:

        # try:
        if request.GET['id']:
            variation = Variation.objects.get(id=int(request.GET['id']))

            data = {
                'price': round(variation.get_variation_product_price(), 2),
                'mrp_price': variation.mrp_price if variation.mrp_price != 0.00 else variation.product.price,
            }

            new_off = ((float(data["price"]) /
                       float(data["mrp_price"])) * 100)-100
            data.update({'off': round(new_off, 2)})
            response = {
                'status': True,
                'data': data
            }
        # except:
        #     response = {
        #         'status':False,
        #         'data':None
        #     }
    return JsonResponse(response)


def cart(request):
    try:
        cart = Cart.objects.get(cart_id = _session_id(request))
    except:
        cart_items = None

    # if not cart.coupon:
    #     request.session['discount_amount'] = 0
    # print(request.session['discount_amount'])
    context = {
        'cart': cart,
    }
    return render(request, 'core/cart.html', context)


def _session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Add to wishlist


@login_required(login_url="userauths:login")
def add_to_wishlist(request):
    product_id = request.GET['id']

    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        wishlist, created = WhishList.objects.get_or_create(
            user=request.user, product=product)
        response = {
            'status': True,
            'message': 'Product added to wishlist',
            'whish_list_count': 1
        }
        return JsonResponse(response)
    else:
        # Redirect to login page or display an error message.
        return redirect('userauths:login')


@login_required(login_url="userauths:login")
def view_wishlist(request):

    products = WhishList.objects.filter(user=request.user)

    context = {'products': products}
    return render(request, 'core/user_account/wishlist.html', context)


@login_required(login_url="userauths:login")
def delete_wishlist_item(request, id):

    wishlist_item = WhishList.objects.get(id=id)

    wishlist_item.delete()
    messages.success(request, "Product removed from wishlist!")
    return redirect("core:wishlist")


@login_required(login_url="userauths:login")
def add_cart_(request):

    if 'discount_amount' in request.session:
        del request.session['discount_amount']
    product_variation = []
    product_id = request.GET['id']
    qty = request.GET['quantity']
    if request.GET['package_size']:
        size = request.GET['package_size']
    else:
        size = None
    # color       = request.GET['color']

    product = Product.objects.get(id=product_id)
    if size is not None:
        print("product have variations...")
        try:
            variation = Variation.objects.get(
                product=product, variation_category__iexact='package_size', pk=size)
            product_variation.append(variation)
        except:
            pass

    try:
        cart = Cart.objects.get(cart_id=_session_id(request))

    except Cart.DoesNotExist:
        if request.user.is_authenticated:
            cart = Cart.objects.create(
                cart_id=_session_id(request),
                user=request.user,
            )
        else:
            cart = Cart.objects.create(
                cart_id=_session_id(request)
            )
    cart.coupon = None
    cart.save()

    is_cart_items_exist = CartItem.objects.filter(
        product=product, cart=cart).exists()
    if is_cart_items_exist:
        # cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        ex_var_list = []
        id = []
        for item in cart_item:
            existing_varaiation = item.variations.all()
            ex_var_list.append(list(existing_varaiation))
            id.append(item.id)

        if size is not None:
            if product_variation in ex_var_list:
                print("product have variations...")
                print(existing_varaiation)
                # increase the item quanity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.qty += int(qty)
                item.save()
                # request.session['order_total'] += item.qty * item.product.discount_price
            else:
                item = CartItem.objects.create(
                    product=product, cart=cart, qty=qty)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    item.save()
        else:
            cart_item.qty += int(qty)
            cart_item.save()

        # if ((product.stock_count)-(cart_item.qty + int(qty))) < 0:
        #     response = {
        #         'status':False,
        #         'message':'Out of Stock'
        #     }
        #     return JsonResponse(response)
        # cart_item.qty += int(qty)

    else:
        if ((product.stock_count) - int(qty)) < 0:
            response = {
                'status': False,
                'message': 'Out of Stock'
            }
            return JsonResponse(response)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            qty=qty
        )
        if size is not None:
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

        cart_item.save()

    response = {
        'status': True,
        'message': 'Product added to Cart',
        'totalcartitems': CartItem.objects.filter(cart=cart).count()
    }
    return JsonResponse(response)


@login_required(login_url="userauths:login")
def increment_cart_item(request):

    qty = 1

    try:
        cart_id = request.GET['cart_id']
        cart_item_id = request.GET['cart_item_id']
        cart = Cart.objects.get(pk=cart_id)
        if 'discount_amount' in request.session:
            del request.session['discount_amount']
            cart.coupon = None
            cart.save()
        cart_item = CartItem.objects.get(pk=cart_item_id)
        if ((cart_item.product.stock_count) - int(cart_item.qty+qty)) < 0:
            response = {
                'status': False,
                'message': 'Out of Stock'
            }
            return JsonResponse(response)
        cart_item.qty += int(qty)
        cart_item.save()
        messages.success(request, "Product quantity incremented")

        response = {
            'status': True,
            'message': 'Product added to Cart',
            'totalcartitems': 1
        }

    except:
        response = {
            'status': False,
            'message': 'Error occured'
        }
    return JsonResponse(response)


def add_cart(request, product_id, qty=1):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id, product=product)

    if not created:
        cart_item.qty += 1
        cart_item.save()

    # return redirect('cart')


def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'product_id': request.GET['id'],
        'qty': request.GET['quantity'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'title': request.GET['title']
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(
                request.GET['id'])]['qty'])+int(cart_data[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    add_cart(request, request.GET['id'], request.GET['quantity'])

    return JsonResponse({"status": True, "message": "Product added to cart!", "data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})


def remove_cart(request):
    try:
        cart_item_id = request.GET['cart_item_id']
        cart_id = request.GET['cart_id']
        cart_item = CartItem.objects.get(id=cart_item_id)
        # Removing applied coupon
        if 'discount_amount' in request.session:
            del request.session['discount_amount']
        cart = Cart.objects.get(pk=cart_id)
        cart.coupon = None
        cart.save()

        if cart_item.qty > 1:
            cart_item.qty -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return JsonResponse({"status": True, "message": "Product removed from cart!"})
    except:
        return JsonResponse({"status": False, "message": "Something error occured try again"})
    
def remove_coupon(request,coupon_id):
    try:
        cart = Cart.objects.get(pk=coupon_id)
        cart.coupon = None
        cart.save()
        if 'discount_amount' in request.session:
            del request.session['discount_amount']
        messages.success(request,'Coupon removed')
        return redirect("core:cart")
    except:
        messages.error(request,'Error Occured!')
        return redirect("core:cart")


def remove_cart_(request):
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            if cart_data[str(request.GET['id'])]['qty'] == 1:
                return delete_cart(request, request.GET['id'])
            if cart_data[str(request.GET['id'])]['qty'] > 1:
                cart_data[str(request.GET['id'])
                          ]['qty'] -= int(str(request.GET['quantity']))
                cart_data.update(cart_data)
                request.session['cart_data_obj'] = cart_data
            else:
                del cart_data[str(request.GET['id'])]

            product = get_object_or_404(Product, id=request.GET['id'])
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
            else:
                cart = Cart.objects.get(session_id=_session_id(request))

            if cart:
                cart_item = CartItem.objects.get(cart=cart, product=product)

                if cart_item.qty > 1:
                    cart_item.qty -= int(request.GET['quantity'])
                    cart_item.save()
                else:
                    cart_item.delete()

    return JsonResponse({"status": True, "message": "Product removed from cart!", "data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})


def delete_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    # cart = get_object_or_404(Product, cart_item_id=cart_item_id)

    cart_item = CartItem.objects.filter(product=product, id=cart_item_id)
    cart_item.delete()

    return JsonResponse({"status": True, "message": "Product removed from cart!"})


@login_required(login_url="userauths:login")
def merge_carts(request):
    print("merging...")
    session_id = request.session.session_key
    carts = CartItem.objects.filter(session_id=session_id)
    for cart in carts:
        cart.session_id = None
        cart.user = request.user
        cart.save()

    return True


@login_required(login_url="userauths:login")
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(
                code=coupon_code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code. Please try again.")
            return redirect('core:cart')

        # Apply the discount here (you may have an order model to store this information).
        # For simplicity, let's assume the order total is stored in the session.
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart.coupon = coupon
        cart.save()
        order_total = sum(item.product.discount_price *
                          item.qty for item in cart_items)
        discount_amount = float(order_total) * (float(coupon.discount) / 100)
        request.session['discount_amount'] = discount_amount

    messages.success(request, "coupon code added")
    # Replace 'checkout' with your checkout page URL.
    return redirect('core:cart')


@login_required(login_url="userauths:login")
def checkout(request):
    try:
        cart = Cart.objects.get(user_id=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

    except:
        messages.error(request, "Your cart is empty")
        return redirect('core:index')

    wallet, created = Wallet.objects.get_or_create(user=request.user)

    if len(cart_items) > 0:
        addresses = Address.objects.filter(user=request.user)
        # merge_carts(request)  # Merge the session cart with the user's cart
        context = {
            'addresses': addresses,
            'wallet': wallet
        }
        return render(request, 'core/checkout.html', context)
    else:
        messages.error(request, "Your cart is empty")
        return redirect('core:index')


@login_required(login_url="userauths:login")
def placeorder(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if cart_items is None:
        messages.error(request, "Your cart is empty!")
        return redirect('core:index')
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        if shipping_address is None:
            messages.error(request, "Please Select Delivery Address")
            return redirect('core:checkout')

        # Fetch user address
        address = Address.objects.get(pk=shipping_address)

        # Calculating Cart Total
        total_amount = 0
        total_mrp_amount = 0
        category_offer = 0
        cart_total = 0
        for item in cart_items:
            try:
                if item.variations.all():
                    for v in item.variations.all():
                        total_amount += item.qty * v.get_variation_product_price()
                        total_mrp_amount += item.qty * v.mrp_price
                else:
                    if item.product.category.offer:
                        total_amount += item.qty * item.product.get_offer_price_by_category()
                        category_offer += item.product.discount_price - \
                            item.product.get_offer_price_by_category()
                    total_mrp_amount += item.product.price * item.qty
            except:
                total_amount += item.product.discount_price * item.qty
                total_mrp_amount += item.product.price * item.qty
        
        final_amount = float(total_amount)
        cart_total = final_amount
        discount_amount = 0
        if 'discount_amount' in request.session and request.session['discount_amount']>0:
            total_amount = float(total_amount)
            final_amount -= float(request.session['discount_amount'])
            discount_amount = request.session['discount_amount']
        
        

        payment_type = request.POST.get('payment_option')
        order = CartOrder.objects.create(
            user=request.user, price=final_amount,coupon_discount=discount_amount, payment_type=payment_type,cart_total=cart_total)

        for i in cart_items:
            try:
                if i.variations.all():
                    for v in i.variations.all():
                        product_price = v.get_variation_product_price()
                else:
                    if i.product.category.offer:
                        product_price = i.product.get_offer_price_by_category()
            except:
                product_price = i.product.discount_price

            product_sub_total = product_price * i.qty

            order_item = CartOrderItems(
                order=order,
                invoice_no="OD-"+order.orderno,
                product=i.product,
                qty=i.qty,
                price=float(product_price),
                total=float(product_sub_total),
                image=i.product.image.url,
            )
            order_item.save()
            cart_item = CartItem.objects.get(id=i.id)
            product_variations = cart_item.variations.all()
            order_item = CartOrderItems.objects.get(id=order_item.id)
            order_item.variations.set(product_variations)
            order_item.save()

            product = get_object_or_404(Product, id=i.product.id)
            if product.stock_count - i.qty >= 0:
                product.stock_count -= i.qty
                product.save()
            else:
                messages.error(request, "some products are out of stock")
                return redirect('core:checkout')

        # Save Shipping address
        order_address = OrderAddress(
            order=order,
            first_name=address.first_name,
            last_name=address.last_name,
            line1=address.line1,
            mobile=address.mobile,
            email=address.email,
            pincode=address.pincode,
            type=address.type,
        )
        order_address.save()
        if cart.coupon:
            coupon = Coupon.objects.get(pk=cart.coupon.id)
            order.coupon = coupon
            order.coupon_discount = request.session['discount_amount']
            order.save()

        if payment_type == 'online':
            return redirect('core:payment', order.orderno)
        elif payment_type == 'wallet':
            user_wallet, created = Wallet.objects.get_or_create(
                user=order.user)
            user_wallet.balance -= order.price
            user_wallet.save()

            user_wallet_transaction = WalletTransaction.objects.create(
                wallet=user_wallet, amount=order.price, type="debited", description='order_placed')
            user_wallet_transaction.save()
        else:
            order.is_ordered = True
            order.save()

        cart.coupon = None
        cart.save()
        cart_items.delete()
        if 'discount_amount' in request.session and request.session['discount_amount'] > 0:
            del request.session['discount_amount']
        messages.success(request, "Your Order placed successfully")
        return redirect('core:checkout_success', order.orderno)
    else:
        return redirect('core:checkout')


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@login_required(login_url="userauths:login")
def payment(request, orderno):
    try:
        oreder = CartOrder.objects.get(orderno=orderno)
    except:
        messages.error(request, "Your order have some problem!")
        return redirect("core:cart")
    context = {
        'order': oreder
    }
    currency = 'INR'
    amount = float(oreder.price)*100  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='1'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    oreder.razorpay_order_id = razorpay_order_id
    oreder.save()

    # callback_url = "http://" + "127.0.0.1:8000" + "/paymenthandler/",
    callback_url = "https://" + "groceryecom.live" + "/paymenthandler/",

    # we need to pass these details to frontend.
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'core/payment.html', context)


@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            order = CartOrder.objects.get(razorpay_order_id=razorpay_order_id)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result:

                try:
                    order.is_ordered = True
                    order.paid_status = True
                    order.save()
                    # capture the payemt
                    # razorpay_client.payment.capture(payment_id, amount)
                    # cart = Cart.objects.get(user=request.user)
                    # cart_items = CartItem.objects.filter(cart=cart)
                    # cart_items.delete()
                    print("suuuu")
                    # render success page on successful caputre of payment
                    messages.success(request, "Your Order placed!")
                    return redirect("core:checkout_success", order.orderno)
                except:

                    # if there is an error while capturing payment.
                    messages.error(request, "Some error occured! 1")
                    return redirect("core:payment", order.orderno)
            else:
                print("error 1")
                # if signature verification fails.
                messages.error(request, "Some error occured! 2")
                return redirect("core:payment", order.orderno)
        except:

            # if we don't find the required parameters in POST data
            print("error 2")
            return redirect("core:payment", order.orderno)
    else:
        print("error 3")
       # if other than POST request is made.
        messages.error(request, "Some error occured! 3")
        return redirect("core:index")


def checkout_success(request, orderno):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart.coupon = None
    cart.save()
    cart_items.delete()
    if 'discount_amount' in request.session and request.session['discount_amount'] > 0:
        del request.session['discount_amount']
    order = CartOrder.objects.get(orderno=orderno)
    context = {
        'order': order
    }
    return render(request, 'core/checkout_success.html', context)
