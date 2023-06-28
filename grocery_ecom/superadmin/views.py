from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address
from core.forms import CategoryForm  

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
            
            messages.success(request, "You are logouted")
            return redirect('superadmin:login')
        else:
            messages.error(request, "You are logouted")
        return redirect('superadmin:category_list')
    categories = Category.objects.all().order_by('-id')
    form = CategoryForm()
    context = {
        'categories': categories,
        'form':form
    }
    return render(request,'admin/category/list.html',context)


############# Logout ###############
def admin_logout(request):
    logout(request)
    messages.success(request, "You are logouted")
    return redirect('superadmin:login')