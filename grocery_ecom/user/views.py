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
    address = Address.objects.filter(user=request.user)
    context = { 
        'addresses':address
    }
    return render(request,'core/user_account/address.html',context)


@login_required(login_url="userauths:login")
def add_address(request):
    form = AddressForm()
    if request.method == 'POST':  
        form = AddressForm(request.POST or None)  
        if form.is_valid():  
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            line1 = form.cleaned_data['line1']
            is_default = form.cleaned_data['is_default']
            type = form.cleaned_data['type']
            pincode = form.cleaned_data['pincode']
            address = Address.objects.create(user=request.user, first_name=first_name,last_name=last_name,email=email,mobile=mobile,line1=line1,is_default=is_default,type=type,pincode=pincode)
            

            # address.save()
            
            messages.success(request, "Address added")
            return redirect('user:address')
        else:
            messages.error(request, 'validation error')
        
        # return redirect('user:add_address')
    context = { 
        'form':form
    }
    return render(request,'core/user_account/add_address.html',context)

@login_required(login_url="userauths:login")
def edit_address(request,id):
    address = Address.objects.get(pk=id)
    data = {
            'first_name' : address.first_name,
            'last_name':address.last_name,
            'pincode':address.pincode,
            'mobile':address.mobile,
            'type':address.type,
            'line1':address.line1,
            'email':address.email,
            'is_default':address.is_default,
        }
    form = AddressForm(instance=address)
    if request.method == 'POST':  
        form = AddressForm(request.POST,initial=data)  
        if form.is_valid():  
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            line1 = form.cleaned_data['line1']
            is_default = form.cleaned_data['is_default']
            type = form.cleaned_data['type']
            pincode = form.cleaned_data['pincode']
            
            if form.has_changed():
                address.first_name = first_name
                address.last_name = last_name
                address.email = email
                address.mobile = mobile
                address.pincode = pincode
                address.line1 = line1
                address.is_default = is_default
                address.type = type

                address.save()
                messages.success(request, "Address updated")
                return redirect('user:address')
            else:
                messages.error(request, "No Changes")
                
        else:
            messages.error(request, 'validation error')
        
    context = { 
        'form':form,
        'address':address
    }
    return render(request,'core/user_account/edit_address.html',context)


@login_required(login_url="userauths:login")
def delete_address(request,id):
    address = Address.objects.get(pk=id)
    address.delete()
    messages.success(request, "Address Deleted!")
    return redirect('user:address')


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
