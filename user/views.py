from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import Category,Vendor,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,Cart,CartItem,OrderCancellationReason,OrderCancellation,Wallet,WalletTransaction
from userauths.models import User
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import AddressForm
from userauths.forms import UserPasswordSetForm

@login_required(login_url="userauths:login")
def account(request):
    context = { 
        
    }
    user_cart = Cart.objects.filter(user=request.user)
    
    return render(request,'core/user_account/account.html',context)


@login_required(login_url="userauths:login")
def address(request):
    address = Address.objects.filter(user=request.user)
    redirect_to = request.GET.get('r')
    context = { 
        'addresses':address
    }
    return render(request,'core/user_account/address.html',context)


@login_required(login_url="userauths:login")
def add_address(request):
    form = AddressForm()
    redirect_to = "address"
    redirect_to = request.GET.get('r')
    if request.method == 'POST':  
        form = AddressForm(request.POST or None)  
        if form.is_valid():  
            first_name  = form.cleaned_data['first_name']
            last_name   = form.cleaned_data['last_name']
            email       = form.cleaned_data['email']
            mobile      = form.cleaned_data['mobile']
            line1       = form.cleaned_data['line1']
            is_default  = form.cleaned_data['is_default']
            type        = form.cleaned_data['type']
            pincode     = form.cleaned_data['pincode']
            address     = Address.objects.create(user=request.user, first_name=first_name,last_name=last_name,email=email,mobile=mobile,line1=line1,is_default=is_default,type=type,pincode=pincode)
            

            # address.save()
            
            messages.success(request, "Address added")
            if redirect_to == 'checkout':
                return redirect('core:'+redirect_to)
            else:
                return redirect('user:address')
            
        else:
            messages.error(request, 'validation error')
        
        # return redirect('user:add_address')
    context = { 
        'form':form,
        'redirect_to':redirect_to
    }
    return render(request,'core/user_account/add_address.html',context)

@login_required(login_url="userauths:login")
def edit_address(request,id):
    address = Address.objects.get(pk=id)
    redirect_to = 'address'
    redirect_to = request.GET.get('r')
    data = {
            'first_name' : address.first_name,
            'last_name':address.last_name,
            'pincode':address.pincode,
            'mobile':address.mobile,
            'type':address.type,
            'line1':address.line1,
            'email':address.email,
            'is_default':bool(address.is_default),
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
                if redirect_to == 'checkout':
                    return redirect('core:'+redirect_to)
                else:
                    return redirect('user:address')
            else:
                messages.error(request, "No Changes")
                
        else:
            messages.error(request, 'validation error')
        
    context = { 
        'form':form,
        'address':address,
        'redirect_to':redirect_to
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
    orders = CartOrder.objects.filter(user=request.user,is_ordered=True).order_by('-id')
    context = { 
        'orders':orders
    }
    return render(request,'core/user_account/orders.html',context)


@login_required(login_url="userauths:login")
def order_details(request,id):
    
    order = CartOrder.objects.get(pk = id)
    context = { 
        'order':order
    }

    return render(request,'core/user_account/order_details.html',context)


@login_required(login_url="userauths:login")
def cancel_order(request,id):
    reasons = OrderCancellationReason.objects.all()
    order = CartOrder.objects.get(pk = id)
    context = { 
        'order':order,
        'reasons':reasons
    }

    return render(request,'core/user_account/cancel_order.html',context)

@login_required(login_url="userauths:login")
def cancel_order_item(request,id):
    
    order_item = CartOrderItems.objects.get(id = id)
    order = CartOrder.objects.get(pk = order_item.order.id)
    # order_items_count = CartOrderItems.objects.filter(order = order).count()
    reason_id = request.GET.get('reson_of_cancel')
    reason = OrderCancellationReason.objects.get(pk = reason_id)
    # if order_item.order.payment_type == 'cod':

    try:
        cancel_request = OrderCancellation.objects.get(order_item = id)
        cancel_request.reason = reason
        cancel_request.status = 'pending'
        cancel_request.save()
    except OrderCancellation.DoesNotExist:
        cancel_request = OrderCancellation.objects.create(
            order_item = order_item,
            reason = reason
        )
        cancel_request.save()
        order.price -= order_item.total
        order.save()
            
    if order_item.order.payment_type == 'online':
        user_wallet, created = Wallet.objects.get_or_create(user=order.user)
        user_wallet.balance += order_item.total
        user_wallet.save()

        user_wallet_transaction = WalletTransaction.objects.create(wallet=user_wallet,amount=order_item.total,type="credited",description = 'order_cancel')
        user_wallet_transaction.save()
        messages.success(request,"Your order was successfully canceled! Amount refunded to your wallet")
    else:
        messages.success(request,"Your order was successfully canceled!")

    return redirect("user:cancel_order_status",id)
    context = { 
        'order':order_item
    }

    return render(request,'core/user_account/cancel_order_item.html',context)

@login_required(login_url="userauths:login")
def cancel_order_status(request,id):
    order_item = CartOrderItems.objects.get(id = id)
    cancel_rquest = OrderCancellation.objects.get(order_item = id)
    context={
        'order_item':order_item,
        'cancel_rquest':cancel_rquest
    }
    return render(request,'core/user_account/cancel_order_status.html',context)



@login_required(login_url="userauths:login")
def profile(request):
    user = User.objects.get(pk = request.user.id)
    context = { 
     'user':user   
    }
    if request.method == 'POST':  
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if first_name == "" or last_name == "":
            messages.error(request, "Please fill all required fields")
            return redirect('user:profile')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, "Profile updated")
        return redirect('user:profile')
    return render(request,'core/user_account/profile.html',context)

@login_required(login_url="userauths:login")
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = UserPasswordSetForm(user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password Chanaged")
            return redirect('user:password_change')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
            return redirect('user:password_change')



    form = UserPasswordSetForm(user)
        
    context = {
        'form':form
    }
            
    return render(request,'core/user_account/password_change.html',context)

def reset_password_change(request):
    user = request.user
    form = UserPasswordSetForm(user)
    if request.method == 'POST':
        email = request.session.get('email')
        try:
            user = User.objects.get(username=email)
        except:
            messages.warning(request,f"User with {email} dose not exist.")
            return redirect("userauths:forgot_password")
    context = {
        'form':form
    }
            
    return render(request,'core/user_account/password_change.html',context)


@login_required(login_url="userauths:login")
def wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
        wallet_transaction = WalletTransaction.objects.filter(wallet=wallet).order_by('-id')
    except:
        wallet = 0
        wallet_transaction = None
    context = { 
        'wallet':wallet,
        'wallet_transaction':wallet_transaction
    }
    return render(request,'core/user_account/wallet.html',context)
