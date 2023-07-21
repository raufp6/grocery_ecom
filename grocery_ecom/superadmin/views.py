from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from core.models import Category,Vendor,Tags,Brand,Product,ProductItem,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,User,Varient,VarientValue
from core.forms import CategoryForm,ProductForm,VarientForm
from django.core.exceptions import ValidationError


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
        'form':form
    }
    return render(request,'admin/category/list.html',context)

def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url="superadmin:login")
def UpdateCategory(request,pk):
    if is_ajax(request):
        category = Category.objects.get(pk=pk)
        data = {
            'title' : category.title,
            'is_featured':category.is_featured,
            'is_available':category.is_available,
            'image':category.image
        }
        form = CategoryForm(request.POST,request.FILES,initial = data)
        if form.is_valid():
            title = form.cleaned_data['title']
            old_title = request.POST.get('old_title')
            is_featured = form.cleaned_data['is_featured']
            is_available = form.cleaned_data['is_available']
            image = request.FILES.get('image')
            if form.has_changed():
                current_title = Category.objects.filter(title = title)
                if old_title != title and Category.objects.filter(title__iexact=title).first():
                    return JsonResponse({'message':'This Category Already Exist!'})
                if old_title != title:
                    category.title = title
                category.is_featured = is_featured
                category.is_available = is_available
                if image is not None:
                    category.image = image
                category.save()
                messages.success(request, "Category updated")
                return JsonResponse({'message':'success'})
            return JsonResponse({'message':'No Changes happen!'})
        return JsonResponse({'message':'Validation error'})
    return JsonResponse({'message':'Worng rquest'})
            


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
    products_items = ProductItem.objects.filter(is_deleted = False,is_default=True).order_by('-id')
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
    return render(request,'admin/product/list.html',context)


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

        check = [title,description,price,discount_price,category,stock_count]
        for values in check:
            if values == '':
                messages.error(request,'some fields are empty')
                return redirect('superadmin:product.create')
        category_instance = Category.objects.get(id=category)
        
        product = Product(
            title = title,
            # brand=brand_instance,
            category=category_instance,
            user = request.user,
            description=description,
            # price=price,
            # discount_price=discount_price,
            # stock_count=stock_count,
            image=image
        )
        product.save()
        
        prd = Product.objects.get(id=product.id)
        product_item = ProductItem(
            title   = title,
            product =   prd,
            price   =   price,
            discount_price  =   discount_price,
            stock_count =   stock_count,
            image   =   image,
            user = request.user,
            is_default  = True
        )
        product_item.save()
        messages.success(request,'Productcreated succefully')
        return redirect('superadmin:product.create')

    categories = Category.objects.filter(is_available = True).order_by('-id')
    form = ProductForm()
    context = {
        'categories': categories,
        'form': form
    }
    
    return render(request,'admin/product/create.html',context)

# Product Update
@login_required(login_url="superadmin:login")
def product_edit(request,id):

    product = Product.objects.get(pk=id)
    # product = Product.objects.get(pk=id,items__is_default=True)
    product_item = product.items.get(is_default=True)
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

        check = [title,description,price,discount_price,category,stock_count]
        for values in check:
            if values == '':
                messages.error(request,'some fields are empty')
                return redirect('superadmin:product.create')
        category_instance = Category.objects.get(id=category)
        
        
        product.title = title
        # brand=brand_instance,
        product.category = category_instance
        product.description = description
        # price=price,
        # discount_price=discount_price,
        # stock_count=stock_count,
        product.image = image
        
        product.save()
        
        product_item.title   = title
        product_item.price   =   price
        product_item.discount_price  =   discount_price
        product_item.stock_count =   stock_count
        product_item.image   =   image
        product_item.save()
        messages.success(request,'Product updated succefully')
        return redirect('superadmin:product_edit',id)

    categories = Category.objects.filter(is_available = True).order_by('-id')
    form = ProductForm()
    context = {
        'categories': categories,
        'form': form,
        'product':product,
        'product_item':product_item
    }
    
    return render(request,'admin/product/edit.html',context)

# Product multiple images
@login_required(login_url="superadmin:login")
def product_images(request,id):

    images = ProductImages.objects.filter(product = id).order_by('-id')
    if request.method == 'POST':
        try:
            image = request.FILES['image']
        except:
            image = ''
            messages.error(request,'Please select a image ')
            return redirect('superadmin:product_images',id)
        
        product_image = ProductImages(
            image =   image,
            product_id = id
            
        )
        product_image.save()
        messages.success(request,'Product Image uploaded succefully')
        return redirect('superadmin:product_images',id)
    
    context = {
        'images': images,
        "id":id
    }
    return render(request,'admin/product/product_images.html',context)


# Delete Product images
@login_required(login_url="superadmin:login")
def delete_product_image(request,id,product_id):
    try:
        image = ProductImages.objects.get(pk = id)
        image.delete()
        messages.success(request,'Product Image deleted succefully')
    except:
        messages.error(request,'Image not found')
    
    return redirect('superadmin:product_images',product_id)

@login_required(login_url="superadmin:login")
def add_product(request):
    if request.method == 'POST':  
        form = ProductForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
            
            messages.success(request, "Product added")
        else:
            messages.error(request, "Please check")
        
        return redirect('superadmin:product.create')
    
# Product Varients
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
        'form':form
    }
    return render(request,'admin/product/varient/list.html',context)


# Product Varient Values
@login_required(login_url="superadmin:login")
def varient_values(request,id):
    varients = VarientValue.objects.filter(varient = id)
    varient = Varient.objects.get(pk=id)
    if request.method == 'POST':  
        
        if request.POST.get('value') == "":
            messages.error(request, "Value field is required")
        else:
            value = request.POST.get('value')
            data = VarientValue.objects.create(
                value = value,
                varient = varient
            )
            data.save()
            messages.success(request, "Value added")
        
        return redirect('superadmin:varient_values',id)
    
    
    context = {
        'varients': varients,
        'varient':varient
    }
    return render(request,'admin/product/varient/varient_values.html',context)

# Product Varient Management
@login_required(login_url="superadmin:login")
def product_varients_manage(request,id):
    varients = Varient.objects.all()
    context = {
        'varients': varients,
        'product_id':id
    }
    return render(request,'admin/product/varient_management.html',context)

# Product Varient Management
@login_required(login_url="superadmin:login")
def varients_values_manage(request,id):
    
    varient_values = []
    if request.method == 'GET':  
        varients_ids = request.GET.getlist('varient')
        varients = Varient.objects.filter(id__in=varients_ids)
        # print(varients)
        for id in varient_values:
            varients = VarientValue.objects.values(varient = id)
            varient_values[varients] = varients
        
        # print(varient_values)

        # for i in varients:
        #     vv = i.varient.all()
        #     for j in vv:
        #         print(j.value)

    context = {
        'varients': varients,
        'varient_values':varient_values,
        'product_id':id
    }
    return render(request,'admin/product/varient_values_manage.html',context)


# Product Varient Value Combination
@login_required(login_url="superadmin:login")
def varients_values_combination(request,id):
    
    varient_values = []
    if request.method == 'GET':  
        varients_ids = request.GET.getlist('varient')
        varients = Varient.objects.filter(id__in=varients_ids)
        # print(varients)
        for id in varient_values:
            varients = VarientValue.objects.values(varient = id)
            varient_values[varients] = varients
        
        # print(varient_values)

        # for i in varients:
        #     vv = i.varient.all()
        #     for j in vv:
        #         print(j.value)

    context = {
        'varients': varients,
        'varient_values':varient_values,
        'product_id':id
    }
    return render(request,'admin/product/varient_values_combination_manage.html',context)




# Order List
@login_required(login_url="superadmin:login")
def order_list(request):
    orders = CartOrder.objects.all()
    context = {
        'orders': orders,
    }
    return render(request,'admin/order/list.html',context)


# Order Details
@login_required(login_url="superadmin:login")
def order_details(request,id):
    order = CartOrder.objects.get(pk=id)
    if request.method == 'POST':  
        status = request.POST.get('order_status')

        order.product_status = status
        order.save()
        messages.success(request, "Order updated")
    
    context = {
        'order': order,
    }
    
    return render(request,'admin/order/details.html',context)
############# Logout ###############
def admin_logout(request):
    logout(request)
    messages.success(request, "You are logouted")
    return redirect('superadmin:login')


class CategoryUpdate(View):
    form_class = CategoryForm

    def is_ajax(self,request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
    def post(self,request,pk,*args,**kwargs):
        if self.is_ajax(request):
            category = Category.objects.get(pk=pk)
            form = self.form_class(request.POST,request.FILES)
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
                return JsonResponse({'message':'success'})
            return JsonResponse({'message':'Validation error'})
            # return JsonResponse({'message':'Worng rquest'})