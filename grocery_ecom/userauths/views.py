from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from core.models import Cart,CartItem
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import random
from core.views import _session_id,merge_carts



User = settings.AUTH_USER_MODEL
User = get_user_model()

def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')   

        try:
            user = User.objects.get(username=email)
        except:
            messages.warning(request,f"User with {email} dose not exist.")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_verified is False:
                messages.error(request,"Your are not verified")
                return redirect('userauths:login')    
            login(request,user)
            # Session cart checking
            merge_carts(request)        
            messages.success(request,"You are loggedIn")
            return redirect('core:index')
        else:
            messages.warning(request,"Invalid email or password")

    
    return render(request,'userauths/login.html')



def register_view(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            
            otp = int(random.randint(1000,9999))

            # Send the OTP to the user via email
            msg = f'OTP Verification, Your OTP is: {otp}' 
            send_mail(
                'Veify Email',
                msg,
                settings.EMAIL_HOST_USER,
                [new_user.username],
                fail_silently=False,
            )

            # Store the OTP in the session for verification
            request.session['otp'] = otp
            request.session['email'] = new_user.username

            # Redirect the user to the OTP verification page
            return redirect('userauths:verify_otp')
        
            # username = form.cleaned_data.get("username")
            # messages.success(request,f"Hey {username} your account was created successfully.")
            # new_user = authenticate(email = form.cleaned_data['email'],
            #                         passwod=form.cleaned_data['password1'])
            # login(request,new_user)
            # return redirect("core:index")

    context = {
        'form':form,
    }
    return render(request,'userauths/sign-up.html',context)


def verify_otp(request):
    if request.method == 'POST':
        user_otp = int(request.POST['otp'])
        saved_otp = request.session.get('otp')
        if user_otp == saved_otp:
            # Verification successful
            email = request.session.get('email')
            # Create the user account or perform any other necessary actions
            # ...

            # Clear the session data
            del request.session['otp']
            del request.session['email']

            user = User.objects.get(username = email)
            messages.success(request,f"Hey {user.first_name} your account was created successfully.")
            login(request,user)

            return redirect("core:index")

        else:
            # Verification failed
            messages.error(request,"Invalid OTP")
            # return redirect('userauths:verify_otp')
    return render(request,'userauths/verify_otp.html')



def user_logout(request):
    logout(request)
    messages.success(request, "You are logout success", extra_tags="success")
    return redirect('userauths:login')
