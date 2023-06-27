from django.shortcuts import render
from django.http import HttpResponse
from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address

def index(request):
    products = Product.objects.filter(featured=True,product_status="published")

    context = { 
        'products':products
    }
    return render(request,'core/index.html',context)

def product_list(request):
    products = Product.objects.filter(product_status="published")

    context = { 
        'products':products
    }
    return render(request,'core/products.html',context)


def category_list(request):
    categories = Category.objects.all()

    context = { 
        'categories':categories
    }
    return render(request,'core/categories.html',context)

# Prodcut Detail
def product_detail(request,pid):
    product = Product.objects.get(pid=pid)
    p_images = product.p_images.all()
    context = { 
        'product':product,
        'p_images': p_images
    }
    return render(request,'core/product-details.html',context)
