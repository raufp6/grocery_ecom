from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL
User = get_user_model()

def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')   

        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request,f"User with {email} dose not exist.")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are loggedIn")
            return redirect('core:index')
        else:
            messages.warning(request,"Invalid email or password")

    
    return render(request,'userauths/login.html')



def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Hey {username} your account was created successfully.")
            new_user = authenticate(username = form.cleaned_data['email'],
                                    passwod=form.cleaned_data['password1'])
            login(request,new_user)
            return redirect("core:index")


    else:    
        form = UserRegisterForm()
    context = {
        'form':form,
    }
    return render(request,'userauths/sign-up.html',context)


def user_logout(request):
    logout(request)
    messages.success(request, "You are logout success", extra_tags="success")
    return redirect('userauths:login')
