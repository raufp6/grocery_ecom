from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("",views.index,name="index"),
    path("products/",views.product_list,name="product_list"),
    path("product/<pid>/",views.product_detail,name="product_detail"),
    path("categories/",views.category_list,name="category_list"),

]