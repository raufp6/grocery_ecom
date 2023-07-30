from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from core.models import Category, Vendor, Tags, Brand, Product, ProductItem, ProductImages, CartOrder, CartOrderItems, ProductReview, WhishList, Countrty, State, City, Address, User, Varient, VarientValue, ProductVarientConfigeration, ProductVarientLink,OrderCancellationReason,OrderCancellation,Coupon,Offer
from core.forms import CategoryForm, ProductForm, VarientForm,CouponForm
from django.core.exceptions import ValidationError
import itertools
from django.template.defaulttags import register


#############  Login ###############
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('superadmin:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(request, username=username, password=password)
        if user_obj and user_obj.is_superuser:
            login(request, user_obj)
            messages.success(request, "You are loggedin to Admin")
            return redirect('superadmin:dashboard')
        else:
            messages.error(request, "Invalid username or password !")
            return redirect('superadmin:login')

    return render(request, 'admin/login.html')

#############  Dashboard ###############


@login_required(login_url="superadmin:login")
def dashboard(request):

    return render(request, 'admin/dashboard.html')


@login_required(login_url="superadmin:login")
def category_list(request):

    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if Category.objects.filter(title__iexact=request.POST.get('title')).first():
            messages.error(request, "Category Already Exist!")
            return redirect('superadmin:category_list')
        if form.is_valid():
            form.save()

            messages.success(request, "Category added")
            return redirect('superadmin:category_list')
        else:
            print(form.errors)
            messages.error(request, form.errors)
        # return redirect('superadmin:category_list')
    categories = Category.objects.all().order_by('-id')

    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'admin/category/list.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="superadmin:login")
def UpdateCategory(request, pk):
    if is_ajax(request):
        category = Category.objects.get(pk=pk)
        data = {
            'title': category.title,
            'is_featured': category.is_featured,
            'is_available': category.is_available,
            'image': category.image
        }
        form = CategoryForm(request.POST, request.FILES, initial=data)
        if form.is_valid():
            title = form.cleaned_data['title']
            old_title = request.POST.get('old_title')
            is_featured = form.cleaned_data['is_featured']
            is_available = form.cleaned_data['is_available']
            image = request.FILES.get('image')
            if form.has_changed():
                current_title = Category.objects.filter(title=title)
                if old_title != title and Category.objects.filter(title__iexact=title).first():
                    return JsonResponse({'message': 'This Category Already Exist!'})
                if old_title != title:
                    category.title = title
                category.is_featured = is_featured
                category.is_available = is_available
                if image is not None:
                    category.image = image
                category.save()
                messages.success(request, "Category updated")
                return JsonResponse({'message': 'success'})
            return JsonResponse({'message': 'No Changes happen!'})
        return JsonResponse({'message': 'Validation error'})
    return JsonResponse({'message': 'Worng rquest'})


############# Users List ###############

@login_required(login_url="superadmin:login")
def users_list(request):
    users = User.objects.filter(is_superuser=0).order_by('-id')
    context = {
        'users': users,
    }
    return render(request, 'admin/user/list.html', context)


@login_required(login_url="superadmin:login")
def block_user(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()

    messages.success(request, "Blocked")
    return redirect('superadmin:users_list')


@login_required(login_url="superadmin:login")
def unblock_user(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()

    messages.success(request, "Unblocked")
    return redirect('superadmin:users_list')


############# Product ###############

@login_required(login_url="superadmin:login")
def product_list(request):
    products = Product.objects.filter(is_deleted=False).order_by('-id')
    products_items = ProductItem.objects.filter(
        is_deleted=False, is_default=True).order_by('-id')
    # for p in products:
    #     prd = Product.objects.get(id=p.id)
    #     product_item = ProductItem(
    #         title   = p.title,
    #         product =   p,
    #         price   =   0,
    #         discount_price  =   0,
    #         stock_count =   10,
    #         image   =   p.image,
    #         is_default  = True
    #     )
    #     product_item.save()
    context = {
        'products': products,
    }
    return render(request, 'admin/product/list.html', context)


@login_required(login_url="superadmin:login")
def create_product(request):

    if request.method == 'POST':
        image = ''
        try:
            image = request.FILES['image']
        except:
            image == 'product.jpg'

        title = request.POST['title']
        category = request.POST['category']
        # brand = request.POST['brand']
        description = request.POST['description']
        price = request.POST['price']
        discount_price = request.POST['discount_price']
        stock_count = request.POST['stock_count']

        check = [title, description, price,
                 discount_price, category, stock_count]
        for values in check:
            if values == '':
                messages.error(request, 'some fields are empty')
                return redirect('superadmin:product.create')
        category_instance = Category.objects.get(id=category)

        product = Product(
            title=title,
            # brand=brand_instance,
            category=category_instance,
            user=request.user,
            description=description,
            # price=price,
            # discount_price=discount_price,
            # stock_count=stock_count,
            image=image
        )
        product.save()

        prd = Product.objects.get(id=product.id)
        product_item = ProductItem(
            title=title,
            product=prd,
            price=price,
            discount_price=discount_price,
            stock_count=stock_count,
            image=image,
            user=request.user,
            is_default=True
        )
        product_item.save()
        messages.success(request, 'Productcreated succefully')
        return redirect('superadmin:product.create')

    categories = Category.objects.filter(is_available=True).order_by('-id')
    form = ProductForm()
    context = {
        'categories': categories,
        'form': form
    }

    return render(request, 'admin/product/create.html', context)

# Product Update


@login_required(login_url="superadmin:login")
def product_edit(request, id):

    product = Product.objects.get(pk=id)
    # product = Product.objects.get(pk=id,items__is_default=True)
    
    # print(product.items)

    if request.method == 'POST':
        try:
            image = request.FILES['image']
        except:
            image = product.image

        title = request.POST['title']
        category = request.POST['category']
        # brand = request.POST['brand']
        description = request.POST['description']
        price = request.POST['price']
        discount_price = request.POST['discount_price']
        stock_count = request.POST['stock_count']

        check = [title, description, price,
                 discount_price, category, stock_count]
        for values in check:
            if values == '':
                messages.error(request, 'some fields are empty')
                return redirect('superadmin:product.create')
        category_instance = Category.objects.get(id=category)

        product.title = title
        # brand=brand_instance,
        product.category = category_instance
        product.description = description
        price=price,
        discount_price=discount_price,
        stock_count=stock_count,
        product.image = image

        product.save()

        messages.success(request, 'Product updated succefully')
        return redirect('superadmin:product_edit', id)

    categories = Category.objects.filter(is_available=True).order_by('-id')
    form = ProductForm()
    context = {
        'categories': categories,
        'form': form,
        'product': product
    }

    return render(request, 'admin/product/edit.html', context)

# Product multiple images


@login_required(login_url="superadmin:login")
def product_images(request, id):

    images = ProductImages.objects.filter(product=id).order_by('-id')
    if request.method == 'POST':
        try:
            image = request.FILES['image']
        except:
            image = ''
            messages.error(request, 'Please select a image ')
            return redirect('superadmin:product_images', id)

        product_image = ProductImages(
            image=image,
            product_id=id

        )
        product_image.save()
        messages.success(request, 'Product Image uploaded succefully')
        return redirect('superadmin:product_images', id)

    context = {
        'images': images,
        "id": id
    }
    return render(request, 'admin/product/product_images.html', context)


# Delete Product images
@login_required(login_url="superadmin:login")
def delete_product_image(request, id, product_id):
    try:
        image = ProductImages.objects.get(pk=id)
        image.delete()
        messages.success(request, 'Product Image deleted succefully')
    except:
        messages.error(request, 'Image not found')

    return redirect('superadmin:product_images', product_id)

# Coupon Management
@login_required(login_url="superadmin:login")
def coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Coupon added")
        else:
            messages.error(request, "Please check")

        return redirect('superadmin:coupons')
    
    coupons = Coupon.objects.all().order_by('-id')
    form = CouponForm()
    context = {
        'coupons':coupons,
        'form':form
    }
    return render(request, 'admin/offer/coupons.html', context)

@login_required(login_url="superadmin:login")
def coupon_update(request,id):
    coupon = Coupon.objects.get(id=id)
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            coupon.code = form.cleaned_data['code']
            coupon.discount = form.cleaned_data['discount']
            coupon.valid_from = form.cleaned_data['valid_from']
            coupon.valid_to = form.cleaned_data['valid_to']
            coupon.active = form.cleaned_data['active']
            coupon.save()
            print(form.cleaned_data['code'])

            messages.success(request, "Coupon added")
        else:
            messages.error(request, "Please check")

        return redirect('superadmin:coupons')
    data = {
        'code':coupon.code,
        'discount':coupon.discount,
        'valid_from':coupon.valid_from,
        'valid_to':coupon.valid_to,
        'active':coupon.active
    }
    form = CouponForm(initial=data)
    context = {
        'coupon':coupon,
        'form':form
    }
    return render(request, 'admin/offer/update_coupon.html', context)


@login_required(login_url="superadmin:login")
def category_offers(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Coupon added")
        else:
            messages.error(request, "Please check")

        return redirect('superadmin:coupons')
    
    offers = Offer.objects.all().order_by('-id')
    form = CouponForm()
    context = {
        'offers':offers,
        'form':form
    }
    return render(request, 'admin/offer/list.html', context)

# Product Variations
@login_required(login_url="superadmin:login")
def product_variations(request, id):
    product = Product.objects.get(pk=id)
    varients = product.prd_varient.values()
    products_items = product.items.filter(is_default=False)
    product_variations_values = VarientValue.objects.values()
    product_variations = Varient.objects.values()
    product_variation_value_dic = {}
    product_variations_dic = {}
    for i in product_variations_values:
        product_variation_value_dic[i['id']] = i['value']

    for i in product_variations:
        product_variations_dic[i['id']] = i['name']
        
    # print(product_variation_dic)
    product_vs = ProductVarientConfigeration.objects.filter(product_item_id = 53)
    # for kk in product_vs:
    #     print(kk.product_item.title)
    #     print(kk.varient_value.value)

    for vv in varients:
        varient = Varient.objects.get(id=int(vv['varient_id']))
        vv['varientInfo'] = varient

    for pvv in product.prd_varient.all():
        print(pvv)

    for p in products_items:
        p_varients = ProductVarientConfigeration.objects.filter(product_item_id=p)
        p_varients = p.prd_varient_values.all()

        for pvv in p.product.prd_varient.all():
            print(pvv.varient_id)
        

        # for pv in p_varients:
        #     print(pv.varient_value_id)
        # print("---")

    context = {
        'products': products_items,
        'product': product,
        'varients': varients,
        'product_vs':product_vs,
        'product_variation_value_dic':product_variation_value_dic,
        'product_variations_dic':product_variations_dic
    }
    return render(request, 'admin/product/variations.html', context)

# Product Varients


@register.filter
def get_item(dictionary, key):
    varient = VarientValue.objects.get(id=key)
    return dictionary.get(key)

@register.filter
def get_varient_name(id):
    varient = varient.objects.get(id=id)
    return varient.name
    


@login_required(login_url="superadmin:login")
def product_varients(request):
    form = VarientForm()
    if request.method == 'POST':
        form = VarientForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Varient added")
        else:
            messages.error(request, "Please check")

        return redirect('superadmin:product_varients')

    varients = Varient.objects.all()
    context = {
        'varients': varients,
        'form': form
    }
    return render(request, 'admin/product/varient/list.html', context)


# Product Varient Values
@login_required(login_url="superadmin:login")
def varient_values(request, id):
    varients = VarientValue.objects.filter(varient=id)
    varient = Varient.objects.get(pk=id)
    if request.method == 'POST':

        if request.POST.get('value') == "":
            messages.error(request, "Value field is required")
        else:
            value = request.POST.get('value')
            data = VarientValue.objects.create(
                value=value,
                varient=varient
            )
            data.save()
            messages.success(request, "Value added")

        return redirect('superadmin:varient_values', id)

    context = {
        'varients': varients,
        'varient': varient
    }
    return render(request, 'admin/product/varient/varient_values.html', context)

# Product Varient Management


@login_required(login_url="superadmin:login")
def product_varients_manage(request, id):
    varients = Varient.objects.all()
    context = {
        'varients': varients,
        'product_id': id
    }
    return render(request, 'admin/product/varient_management.html', context)

# Product Varient Management


@login_required(login_url="superadmin:login")
def varients_values_manage(request, id):

    varient_values = []
    if request.method == 'GET':
        varients_ids = request.GET.getlist('varient')
        varients = Varient.objects.filter(id__in=varients_ids)
        # print(varients)
        for id in varient_values:
            varients = VarientValue.objects.values(varient=id)
            varient_values[varients] = varients

        # print(varient_values)

        # for i in varients:
        #     vv = i.varient.all()
        #     for j in vv:
        #         print(j.value)

    context = {
        'varients': varients,
        'varient_values': varient_values,
        'product_id': id
    }
    return render(request, 'admin/product/varient_values_manage.html', context)


# Product Varient Value Combination
@login_required(login_url="superadmin:login")
def varients_values_combination(request, id):

    varient_values = {}
    varient_values_combinations = {}
    if request.method == 'GET':
        varients_ids = request.GET.getlist('varient[]')
        for i in varients_ids:
            varient_values[i] = request.GET.getlist('varient_value['+i+']')
        # print(varients_ids)
        # print(varient_values)

    product = Product.objects.get(pk=id)
    product_item = product.items.get(is_default=True)
    combinations = list(itertools.product(
        varient_values[varients_ids[0]], varient_values[varients_ids[1]]))
    html = '<input type="hidden" name="selected_variations" value="' + \
        convertTupleToString(varients_ids)+'">'
    k = 0
    # print(combinations)
    for item in combinations:
        k += 1
        combo_values = convertTupleToString(item)

        html += '<tr>'
        html += '<input type="hidden" name="option_values_comb" value="'+combo_values+'">'
        html += '<td><input type="text" class="form-control" name="product_item_title" value="'+product.title+'"></td><td><input type="text" class="form-control" name="product_item_price" value="' + \
            str(product_item.price)+'"></td><td><input type="text" class="form-control" name="product_item_dicount_price" value="'+str(product_item.discount_price) + \
            '"></td><td><input type="text" class="form-control" name="product_item_stock" value="' + \
            str(product_item.stock_count)+'"></td>'
        html += '</tr>'
    context = {
        'varient_values': varient_values,
        'product_id': id,
        'product': product,
        'combinations': combinations,
        'html': html
    }
    return render(request, 'admin/product/varient_values_combination_manage.html', context)


def convertTupleToString(tup):
    # initialize an empty string
    str = ''
    for item in tup:
        str = str + "," + item
    return str[1:]

# Product Varient Value Combination


@login_required(login_url="superadmin:login")
def generate_varients(request, id):
    if request.method == 'GET':
        selected_variations = request.GET.get('selected_variations')
        option_values_comb = request.GET.getlist('option_values_comb')
        product_item_title = request.GET.getlist('product_item_title')
        product_item_price = request.GET.getlist('product_item_price')
        product_item_dicount_price = request.GET.getlist(
            'product_item_dicount_price')
        product_item_stock = request.GET.getlist('product_item_stock')

    prd = Product.objects.get(id=id)
    selected_variations_li = list(selected_variations.split(","))
    for svi in selected_variations_li:
        prd_variation_link_data = ProductVarientLink.objects.create(
            product=prd,
            varient_id=svi
        )
        prd_variation_link_data.save()
    for i in range(len(option_values_comb)):
        # print(option_values_comb[i])
        # print(list(option_values_comb[i]))
        varient_values_li = list(option_values_comb[i].split(","))
        # print(type(varient_values_li))
        # print(varient_values_li)

        product_item = ProductItem(
            title=product_item_title[i],
            product=prd,
            price=product_item_price[i],
            discount_price=product_item_dicount_price[i],
            stock_count=product_item_stock[i],
            image=prd.image,
            user=request.user,
            is_default=False
        )
        product_item.save()
        for k in varient_values_li:
            # k = k.replace("'",'')
            # print(k)
            # print(type(int(k)))
            # print(option_values_comb[i])
            product_conf = ProductVarientConfigeration(
                product_item=product_item,
                varient_value_id=k
            )
            product_conf.save()

    # print(type(option_values_comb[0]))
    return HttpResponse(option_values_comb)


# Order List
@login_required(login_url="superadmin:login")
def order_list(request):
    orders = CartOrder.objects.all().order_by('-id')
    context = {
        'orders': orders,
    }
    return render(request, 'admin/order/list.html', context)


# Order Details
@login_required(login_url="superadmin:login")
def order_details(request, id):
    order = CartOrder.objects.get(pk=id)
    if request.method == 'POST':
        status = request.POST.get('order_status')

        order.product_status = status
        order.save()
        messages.success(request, "Order updated")

    context = {
        'order': order,
    }

    return render(request, 'admin/order/details.html', context)


# Order Cancelation Request
@login_required(login_url="superadmin:login")
def order_cancel_request(request, id):
    request_item = OrderCancellation.objects.get(pk=id)

    if request.method == 'POST':
        status = request.POST.get('status')
        request_item.status = status
        request_item.save()
        messages.success(request, "Order updated")
        

        

    context = {
        'request_item': request_item,
    }

    return render(request, 'admin/order/cancel_request.html', context)

############# Logout ###############


def admin_logout(request):
    logout(request)
    messages.success(request, "You are logouted")
    return redirect('superadmin:login')


class CategoryUpdate(View):
    form_class = CategoryForm

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def post(self, request, pk, *args, **kwargs):
        if self.is_ajax(request):
            category = Category.objects.get(pk=pk)
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                is_featured = form.cleaned_data['is_featured']
                is_available = form.cleaned_data['is_available']
                image = request.FILES.get('image')

                category.title = title
                category.is_featured = is_featured
                category.is_available = is_available
                if image is not None:
                    category.image = image
                category.save()
                return JsonResponse({'message': 'success'})
            return JsonResponse({'message': 'Validation error'})
            # return JsonResponse({'message':'Worng rquest'})
