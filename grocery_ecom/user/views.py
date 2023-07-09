from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,Cart,CartItem
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import AddressForm

@login_required(login_url="userauths:login")
def account(request):
    context = { 
        
    }
    user_cart = Cart.objects.filter(user=request.user)
    
    return render(request,'core/user_account/account.html',context)


@login_required(login_url="userauths:login")
def address(request):
    context = { 
        
    }
    return render(request,'core/user_account/address.html',context)


@login_required(login_url="userauths:login")
def add_address(request):
    form = AddressForm()
    if request.method == 'POST':  
        form = AddressForm(request.POST)  
        if form.is_valid():  
            form.save()  
            
            messages.success(request, "Address added")
        else:
            messages.error(request, form.errors)
        
        return redirect('user:add_address')
    context = { 
        
    }
    return render(request,'core/user_account/add_address.html',context)

@login_required(login_url="userauths:login")
def orders(request):
    context = { 
        
    }
    return render(request,'core/user_account/address.html',context)

@login_required(login_url="userauths:login")
def profile(request):
    context = { 
        
    }
    return render(request,'core/user_account/address.html',context)
