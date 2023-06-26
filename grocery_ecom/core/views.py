from django.shortcuts import render
from django.http import HttpResponse
from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address

def index(request):
    products = Product.objects.all()

    context = { 
        'products':products
    }
    return render(request,'core/index.html',context)
