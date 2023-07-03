from django.urls import path
from superadmin import views

app_name = "superadmin"

urlpatterns = [
    path("", views.admin_login, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("category_list", views.category_list, name="category_list"),
    path("users_list", views.users_list, name="users_list"),
    path("blockuser/<int:id>", views.block_user, name="block_user"),
    path("unblock_user/<int:id>", views.unblock_user, name="unblock_user"),

    path("product_list", views.product_list, name="product_list"),
    path("product/create/", views.creat_product, name="product.create"),
    path("add_product", views.add_product, name="add_product"),
    path('logout', views.admin_logout, name='logout'),

]
