from django.db import models
from django import forms
from core.models import Category, Product, Address,ProductItem,Coupon,Offer
from django.forms import fields
from django.core.validators import FileExtensionValidator
from ckeditor_uploader.widgets import CKEditorUploadingWidget


categories = Category.objects.filter(is_featured=True)

ADDRESS_TYPES = (
    ("home", "Home"),
    ("office", "Office")
)

FAVORITE_COLORS_CHOICES = [
    ("blue", "Blue"),
    ("green", "Green"),
    ("black", "Black"),
]
STATUS = [
    ('true', 'Yes'), ('false', 'No')
]




class CategoryForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Title", 'class': "form-control"}),
        error_messages={
            'required': "Please Enter category Title"
        },
    )
    # image = forms.ImageField(widget = forms.FileInput(attrs={'class':'form-control'}),required=True,validators=[FileExtensionValidator(['jpg', 'png','webp','jpeg', 'svg'])])
    is_featured = forms.CheckboxInput()

    class Meta:
        model = Category
        fields = ['title', 'is_featured', 'image', 'is_available']

        # fields = "__all__"

        widgets = {
            'is_available': forms.Select(attrs={'class': 'form-control', 'id': 'choicewa'}, choices=STATUS),
        }



class CouponForm(forms.ModelForm):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Coupon Code", 'class': "form-control"}),
        error_messages={
            'required': "Please Enter Coupon Code"
        },
    )
    discount = forms.DecimalField(
        widget=forms.TextInput(
            attrs={'placeholder': "Discount", 'class': "form-control"}),
        error_messages={
            'required': "Please Enter Discount"
        },
    )
    
    valid_from = forms.DateField(
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'placeholder': "Valid from", 'class': "form-control","type":'date'}),
        error_messages={
            'required': "Please Enter valid from date"
        },
    )
    valid_to = forms.DateField(
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'placeholder': "Valid from", 'class': "form-control","type":'date'}),
        error_messages={
            'required': "Please Enter valid from date"
        },
    )
    class Meta:
        model = Coupon
        fields = "__all__"

        

class OfferForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Offer Name", 'class': "form-control"}),
        error_messages={
            'required': "Please Enter Offer Name"
        },
    )    
    off_percent = forms.DecimalField(
        widget=forms.TextInput(
            attrs={'placeholder': "Discount", 'class': "form-control"}),
        error_messages={
            'required': "Please Enter Discount"
        },
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'placeholder': "Valid from", 'class': "form-control","type":'date'}),
        error_messages={
            'required': "Please Enter valid from date"
        },
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'placeholder': "Valid from", 'class': "form-control","type":'date'}),
        error_messages={
            'required': "Please Enter valid from date"
        },
    )
    class Meta:
        model = Offer
        fields = "__all__"
        # fields = ['name', 'off_percent', 'start_date', 'end_date','category']


        

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Title", 'class': "form-control"}))
    price = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Prodcut Price", 'class': "form-control"}))
    discount_price = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Prodcut Price", 'class': "form-control"}))
    stock_count = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': "Prodcut Stock", 'class': "form-control"}))
    image = forms.ImageField()
    life = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Prodcut Life", 'class': "form-control"}))
    category = forms.ChoiceField(choices=categories)
    # mfd = forms.DateField()

    class Meta:
        model = Product
        fields = ['title', 'stock_count', 'image',
                  'description', 'category', 'mfd', 'life']
        # fields = "__all__"
        widgets = {
            'mfd': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                       }),
        }

class ProductItemForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Title", 'class': "form-control"}))
    price = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Prodcut Price", 'class': "form-control"}))
    discount_price = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Prodcut Price", 'class': "form-control"}))
    stock_count = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': "Prodcut Stock", 'class': "form-control"}))
    image = forms.ImageField()
    category = forms.ChoiceField(choices=categories)
    # mfd = forms.DateField()

    class Meta:
        model = Product
        fields = ['title', 'stock_count', 'image']
        


class AddressForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "First Name"}),
        error_messages={
            'required': "Please Enter First Name"
        },
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Last Name"}),
        error_messages={
            'required': "Please Enter Last name"
        },
    )
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Mobile Number"}),
        error_messages={
            'required': "Please Enter Mobile"
        },
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'placeholder': "Email", 'class': "email_validate"}),
        error_messages={
            'required': "Please Enter Email"
        },
    )
    line1 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Address"}),
        error_messages={
            'required': "Please Enter Address"
        },
    )
    pincode = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Pincode"}),
        error_messages={
            'required': "Please Enter Pincode"
        },
    )
    is_default = forms.BooleanField(required=False,
            widget=forms.CheckboxInput(attrs={'class':'form-check-input','id':'exampleCheckbox12','value':'true'}),
    )
    type = forms.ChoiceField(choices=ADDRESS_TYPES, widget=forms.Select(
        attrs={'placeholder': "Select", 'class': 'form-control'}))

    class Meta:
        model = Address
        fields = ['mobile', 'email', 'first_name',
                  'last_name', 'line1', 'pincode', 'type','is_default']
