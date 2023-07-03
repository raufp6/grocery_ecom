from django.db import models  
from django import forms
from core.models import Category,Product
from django.forms import fields 
from django.core.validators import FileExtensionValidator 
from ckeditor_uploader.widgets import CKEditorUploadingWidget

categories = Category.objects.filter(is_featured=True)


class CategoryForm(forms.ModelForm):
    pass
    # title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title",'class':"form-control"}))
    # image = forms.ImageField()
    # is_featured = forms.CheckboxInput()
    # class Meta:
    #     model = Category
    #     fields = ['title','is_featured','image']


class ProductForm(forms.ModelForm):
    pass
    # description = forms.CharField(widget=CKEditorUploadingWidget())
    # title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title",'class':"form-control"}))
    # price = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Prodcut Price",'class':"form-control"}))
    # discount_price = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Prodcut Price",'class':"form-control"}))
    # stock_count = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Prodcut Stock",'class':"form-control"}))
    # image = forms.ImageField()
    # category = forms.ChoiceField(choices = categories)

    # class Meta:
    #     model = Product
    #     fields = ['title','stock_count','image','description','category']