from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("",views.index,name="index"),
    path("products/",views.product_list,name="product_list"),
    path("pd/<pid>/<str:slug>/",views.product_detail_new,name="product_detail"),
    path("categories/",views.category_list,name="category_list"),
    
    #Cart
    # path("add-to-cart/",views.add_to_cart_,name="add-to-cart"),
    path("add_to_cart/",views.add_to_cart,name="add-to-cart"),
    path("remove_cart/",views.remove_cart,name="remove_cart"),
    path("delete_cart/<int:product_id>/",views.delete_cart,name="delete_cart"),
    
    path("cart/",views.cart,name="cart"),


]