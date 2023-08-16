from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from core.models import Category, Vendor, Brand, Product, ProductItem, ProductImages, CartOrder, CartOrderItems, ProductReview, WhishList, Countrty, State, City, Address, User,OrderCancellationReason,OrderCancellation,Coupon,Offer
from core.forms import CategoryForm, ProductForm,CouponForm,OfferForm
from django.core.exceptions import ValidationError
import itertools
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.db.models import Sum, F
from django.db.models.functions import TruncDate
from reportlab.pdfgen import canvas
from io import BytesIO
import openpyxl
import calendar
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import timedelta


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
    revenue = CartOrderItems.objects.filter(product_status='completed').aggregate(sum=Sum(F('price')*F('qty')))["sum"]
    total_completed_order = CartOrder.objects.filter(product_status='completed').count()
    product_count = Product.objects.count()
    user_count = User.objects.count()
    recent_sale = CartOrder.objects.all().order_by('-id')[:5]
    
    # sale report by month for graph
    today = timezone.now().date()
    five_months_ago = today - timedelta(days=150)
    sales_report = (
    CartOrder.objects
    .annotate(month=TruncMonth('order_date'))
    .filter(order_date__gte=five_months_ago, product_status='completed')
    .values(month = F('month__month'))
    .annotate(total_sales=Sum('price'))
    .order_by('month')
    )

    for entry in sales_report:
        entry['month_name'] = get_month_name(entry['month'])

    print(sales_report)

    context = {
        'revenue':revenue,
        'total_completed_order':total_completed_order,
        'product_count':product_count,
        'user_count':user_count,
        'recent_sale':recent_sale
    }
    return render(request, 'admin/dashboard.html',context)


# for getting month name--------------------------------------



def get_month_name(month_number):
    if 1 <= month_number <= 12:
        return calendar.month_name[month_number]
    else:
        return None

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
    p = Paginator(products, 10) 
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        'products': products,
        'page_obj':page_obj
    }
    print(p.page_range)
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
            price=price,
            discount_price=discount_price,
            stock_count=stock_count,
            image=image
        )
        product.save()

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
    print(id)
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
            # print(form.cleaned_data['code'])

            messages.success(request, "Coupon updated")
        else:
            messages.error(request, "Check all field")

        # return redirect('superadmin:coupons')
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
        'form':form,
        'data':data
    }
    return render(request, 'admin/offer/update_coupon.html', context)


@login_required(login_url="superadmin:login")
def category_offers(request):
    form = OfferForm()
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Category offer added")
        else:
            
            messages.error(request, form.errors)


        # return redirect('superadmin:category_offers')
    
    offers = Offer.objects.all().order_by('-id')
    
    categories = Category.objects.all().order_by('-id')
    context = {
        'offers':offers,
        'form':form,
        'categories':categories
    }
    return render(request, 'admin/offer/list.html', context)


@login_required(login_url="superadmin:login")
def update_category_offer(request,id):
    offer = Offer.objects.get(id=id)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            
            offer.name = form.cleaned_data['name']
            offer.off_percent = form.cleaned_data['off_percent']
            offer.start_date = form.cleaned_data['start_date']
            offer.category = form.cleaned_data['category']
            offer.end_date = form.cleaned_data['end_date']
            offer.active = form.cleaned_data['active']
            offer.save()

            messages.success(request, "Category offer updated")
        else:
            print(form.errors)
            
            messages.error(request, form.errors)

        # return redirect('superadmin:coupons')
    data = {
        'name':offer.name,
        'off_percent':offer.off_percent,
        'start_date':offer.start_date,
        'category':offer.category,
        'end_date':offer.end_date,
        'active':offer.active
    }
    form = OfferForm(initial=data)
    categories = Category.objects.all().order_by('-id')
    
    context = {
        'offer':offer,
        'form':form,
        'data':data,
        'categories':categories
    }
    return render(request, 'admin/offer/update_offer.html', context)





def convertTupleToString(tup):
    # initialize an empty string
    str = ''
    for item in tup:
        str = str + "," + item
    return str[1:]


# Order List
@login_required(login_url="superadmin:login")
def order_list(request):
    orders = CartOrder.objects.filter(is_ordered = True).order_by('-id')
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
        if status == 'completed':
            order_items = order.order_items.all()
            for item in order_items:
                item.product_status = status
                item.save()
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


def sales_report(request):
    orders = CartOrder.objects.filter(product_status='completed').order_by('-id')
    # sales_data = CartOrder.objects.values('user').annotate(Sum('price'))
    start_date = request.GET.get('from')
    end_date = request.GET.get('to')
    
    if start_date is not None or end_date is not None:
        order_items = CartOrderItems.objects.filter(order__order_date__gte=start_date, order__order_date__lte=end_date,order__product_status='completed')
    else:
        order_items = CartOrderItems.objects.filter(order__product_status='completed')
    context = {
        'orders': orders,
        'order_items':order_items
    }
    
    return render(request, 'admin/report/sales.html', context)


def sales_report_pdf(request):
    start_date = request.GET.get('from')
    end_date = request.GET.get('to')
    
    if start_date is not None or end_date is not None:
        order_items = CartOrderItems.objects.filter(order__order_date__gte=start_date, order__order_date__lte=end_date,order__product_status='completed')
    else:
        order_items = CartOrderItems.objects.filter(order__product_status='completed')
    
    
    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.drawString(72, 800, "Sales Report")
    pdf.drawString(72, 770, "OrderNo")
    pdf.drawString(200, 770, "Product")
    pdf.drawString(500, 770, "Total")
    pdf.drawString(600, 770, "Date")

    y = 750
    for entry in order_items:
        
        date_str = entry.order.order_date.strftime('%Y-%m-%d')
        pdf.drawString(72, y, str(entry.order.orderno))
        pdf.drawString(200, y, str(entry.product.title))
        pdf.drawString(500, y, str(entry.price))
        pdf.drawString(600, y, date_str)
        
        y -= 20

    pdf.save()
    pdf_buffer = buffer.getvalue()
    buffer.close()
    response.write(pdf_buffer)
    return response


def sales_report_excel(request):
    start_date = request.GET.get('from')
    end_date = request.GET.get('to')
    
    if start_date is not None or end_date is not None:
        order_items = CartOrderItems.objects.filter(order__order_date__gte=start_date, order__order_date__lte=end_date,order__product_status='completed')
    else:
        order_items = CartOrderItems.objects.filter(order__product_status='completed')

    # Generate Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    worksheet.append(["Order No","Product","Price", "Date"])
    for entry in order_items:
        date_str = entry.order.order_date.strftime('%Y-%m-%d')
        worksheet.append([entry.order.orderno,entry.product.title,entry.price,date_str])

    excel_file = BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)
    response.write(excel_file.getvalue())
    excel_file.close()
    return response

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
