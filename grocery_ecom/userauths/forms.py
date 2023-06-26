from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Username"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Last Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email",'class':"email_validate"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Confirm Password"}))
    agrrement = forms.BooleanField(required=False)
   
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']