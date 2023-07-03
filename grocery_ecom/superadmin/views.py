from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,User
from core.forms import CategoryForm,ProductForm


#############  Login ###############
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('superadmin:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password =  request.POST.get('password')
        user_obj = authenticate(request, username=username, password=password)
        if user_obj and user_obj.is_superuser:
            login(request, user_obj)
            messages.success(request, "You are loggedin to Admin")
            return redirect('superadmin:dashboard')
        else:
            messages.error(request, "Invalid username or password !")
            return redirect('superadmin:login')
    
    return render(request,'admin/login.html')

#############  Dashboard ###############
@login_required(login_url="superadmin:login")
def dashboard(request):

    return render(request,'admin/dashboard.html')

@login_required(login_url="superadmin:login")
def category_list(request):
    if request.method == 'POST':  
        form = CategoryForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
            
            messages.success(request, "Category added")
            return redirect('superadmin:login')
        else:
            messages.error(request, "Error")
        return redirect('superadmin:category_list')
    categories = Category.objects.all().order_by('-id')
    form = CategoryForm()
    context = {
        'categories': categories,
        'form':form
    }
    return render(request,'admin/category/list.html',context)


############# Users List ###############

@login_required(login_url="superadmin:login")
def users_list(request):
    users = User.objects.filter(is_superuser = 0).order_by('-id')
    context = {
        'users': users,
    }
    return render(request,'admin/user/list.html',context)

@login_required(login_url="superadmin:login")
def block_user(request,id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()

    messages.success(request, "Blocked")
    return redirect('superadmin:users_list')

@login_required(login_url="superadmin:login")
def unblock_user(request,id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()

    messages.success(request, "Unblocked")
    return redirect('superadmin:users_list')



############# Product ###############

@login_required(login_url="superadmin:login")
def product_list(request):
    products = Product.objects.filter(is_deleted = False).order_by('-id')
    context = {
        'products': products,
    }
    return render(request,'admin/product/list.html',context)


@login_required(login_url="superadmin:login")
def creat_product(request):

    if request.method == 'POST':
        image = ''
        try:
            image = request.FILES['image']
        except:
            if image == '':
                messages.info(request,"Image field can't be empty")
                return redirect('superadmin:product.create')
        
        title = request.POST['title']
        category = request.POST['category']
        # brand = request.POST['brand']
        category = request.POST['category']
        description = request.POST['description']
        price = request.POST['price']
        discount_price = request.POST['discount_price']
        stock_count = request.POST['stock_count']

        check = [title,description,price,discount_price,category,stock_count]
        for values in check:
            if values == '':
                messages.error(request,'some fields are empty')
                return redirect('superadmin:product.create')
        category_instance = Category.objects.get(id=category)
        print(category_instance)
        # Product.objects.create(
        #     title = title,
        #     # brand=brand_instance,
        #     category=category_instance,
        #     description=description,
        #     price=price,
        #     discount_price=discount_price,
        #     stock_count=stock_count,
        #     image=image
        # ).save()
        messages.success(request,'Productcreated succefully')
        return redirect('superadmin:product.create')

    categories = Category.objects.all().order_by('-id')
    form = ProductForm()
    context = {
        'categories': categories,
        'form': form
    }
    
    return render(request,'admin/product/create.html',context)


def add_product(request):
    if request.method == 'POST':  
        form = ProductForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
            
            messages.success(request, "Product added")
        else:
            messages.error(request, "Olease check")
        
        return redirect('superadmin:product.create')


############# Logout ###############
def admin_logout(request):
    logout(request)
    messages.success(request, "You are logouted")
    return redirect('superadmin:login')