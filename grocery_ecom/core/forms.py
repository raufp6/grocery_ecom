from django.db import models  
from django import forms
from core.models import Category,Product
from django.forms import fields 
from django.core.validators import FileExtensionValidator 
from ckeditor_uploader.widgets import CKEditorUploadingWidget


categories = Category.objects.filter(is_featured=True)

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
        widget=forms.TextInput(attrs={'placeholder':"Title",'class':"form-control"}),
        error_messages = {
            'required':"Please Enter category Title"
        },
    )
    # image = forms.ImageField(widget = forms.FileInput(attrs={'class':'form-control'}),required=True,validators=[FileExtensionValidator(['jpg', 'png','webp','jpeg', 'svg'])])
    is_featured = forms.CheckboxInput()
    
    
    
    class Meta:
        model = Category
        fields = ['title','is_featured','image','is_available']

        # fields = "__all__"

        widgets = {
            'is_available': forms.Select(attrs={'class':'form-control','id':'choicewa'},choices=STATUS),
        }
        


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title",'class':"form-control"}))
    price = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Prodcut Price",'class':"form-control"}))
    discount_price = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Prodcut Price",'class':"form-control"}))
    stock_count = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Prodcut Stock",'class':"form-control"}))
    image = forms.ImageField()
    life = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Prodcut Life",'class':"form-control"}))
    category = forms.ChoiceField(choices = categories)
    # mfd = forms.DateField()

    class Meta:
        model = Product
        fields = ['title','stock_count','image','description','category','mfd','life']
        # fields = "__all__"
        widgets = {
            'mfd': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
        }