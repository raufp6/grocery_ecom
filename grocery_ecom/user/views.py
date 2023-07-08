from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,Cart,CartItem
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required

@login_required(login_url="superadmin:login")
def account(request):
    pass
