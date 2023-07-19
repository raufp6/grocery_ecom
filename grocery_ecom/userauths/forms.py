from django import forms
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm,PasswordResetForm
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


class UserPasswordSetForm(SetPasswordForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Confirm Password"}))
    class Meta:
        model = User
        fields = ['password1','password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())