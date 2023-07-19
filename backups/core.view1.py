from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from core.models import Category, Vendor, Tags, Brand, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, WhishList, Countrty, State, City, Address, Cart, CartItem
from django.template.defaultfilters import slugify
# from cart.cart import Cart
from django.db.models import Q


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


def category_list(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'core/categories.html', context)

# Prodcut Detail


def product_detail(request, id, slug):
    product = Product.objects.get(id=id)
    p_images = product.p_images.all()
    context = {
        'product': product,
        'p_images': p_images
    }
    return render(request, 'core/product-details.html', context)


def product_detail_new(request, pid, slug):
    product = Product.objects.get(pid=pid)
    p_images = product.p_images.all()
    context = {
        'product': product,
        'p_images': p_images
    }
    return render(request, 'core/product-details.html', context)


def cart(request):

    context = {

    }
    return render(request, 'core/cart.html', context)


def _session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id, qty=1):
    product = Product.objects.get(id=product_id)
    # try:
    #     # cart = Cart.objects.get(session_id=_session_id(request))
    #     cart_item = CartItem.objects.get(product=product, session_id=_session_id(request))

    # except CartItem.DoesNotExist:
    #     if request.user.is_authenticated:
    #         cart = CartItem.objects.create(
    #             user = request.user,
    #             product = product,
    #             qty = 1
    #         )
    #     else:
    #         cart = CartItem.objects.create(
    #             session_id = _session_id(request),
    #             product = product,
    #             qty = 1
    #         )
    # cart.save()

    try:
        cart_item = CartItem.objects.get(
            product=product, session_id=_session_id(request))
        if ((product.stock_count)-(cart_item.qty + int(qty))) < 0:
            response = {
                'status': False,
                'message': 'Out of Stock'
            }
            return response
        cart_item.qty += int(qty)
        cart_item.save()
    except CartItem.DoesNotExist:
        if ((product.stock_count) - int(qty)) < 0:
            response = {
                'status': False,
                'message': 'Out of Stock'
            }
            return response
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(
                product=product,
                qty=qty,
                user=request.user
            )
        else:
            cart = CartItem.objects.create(
                session_id=_session_id(request),
                product=product,
                qty=qty
            )
        cart_item.save()
        response = {
            'status': True,
            'message': 'added'
        }
        return response


def add_cart__(request, product_id, qty=1):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart_item, created = Cart.objects.get_or_create(
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
    # if request.user.is_authenticated:
    add_cart(request, request.GET['id'], request.GET['quantity'])

    return JsonResponse({"status": True, "message": "Product added to cart!", "data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})


def remove_cart(request):
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


def delete_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if 'cart_data_obj' in request.session:
        if str(product_id) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del cart_data[str(product_id)]
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(session_id=_session_id(request))

    cart_item = CartItem.objects.filter(product=product, cart=cart)
    cart_item.delete()

    return JsonResponse({"status": True, "message": "Product removed from cart!", "data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})