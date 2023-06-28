from django.db import models  
from django import forms
from core.models import Category
from django.forms import fields 
from django.core.validators import FileExtensionValidator 

class CategoryForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title",'class':"form-control"}))
    image = forms.ImageField()
    is_featured = forms.CheckboxInput()
    class Meta:
        model = Category
        fields = ['title','is_featured','image']