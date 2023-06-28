from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
# from phone_field import PhoneField
# from phonenumber_field.modelfields import PhoneNumberField

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Last Name"}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Mobile Number"}))
    username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email",'class':"email_validate"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Confirm Password"}))
    agrrement = forms.BooleanField(required=False)
   
    class Meta:
        model = User
        fields = ['mobile','username','first_name','last_name']