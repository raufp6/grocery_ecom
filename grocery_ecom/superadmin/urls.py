from django.urls import path
from superadmin import views
from .views import (CategoryUpdate)

app_name = "superadmin"

urlpatterns = [
    path("", views.admin_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # Category
    path("category_list/", views.category_list, name="category_list"),
    # path("category/update/<int:pk>/", CategoryUpdate.as_view(), name="update_category"),
    path("category/update/<int:pk>/", views.UpdateCategory, name="update_category"),

    path("users_list/", views.users_list, name="users_list"),
    path("blockuser/<int:id>", views.block_user, name="block_user"),
    path("unblock_user/<int:id>", views.unblock_user, name="unblock_user"),

    #Orders
    path("order/list/", views.order_list, name="order_list"),
    path("order/details/<int:id>", views.order_details, name="order_details"),
    path("order/cancel_request/<int:id>/", views.order_cancel_request, name="order_cancel_request"),

    path("product_list/", views.product_list, name="product_list"),
    path("product/create/", views.create_product, name="product.create"),
    path("product/edit/<int:id>/", views.product_edit, name="product_edit"),
    path("product/images/<int:id>/", views.product_images, name="product_images"),
    path("product/image/delete/<int:id>/<int:product_id>/", views.delete_product_image, name="delete_product_image"),

    path("product_variations/<int:id>/", views.product_variations, name="product_variations"),
    path("product/varients/<int:id>/", views.product_varients_manage, name="product_varient_manage"),
    path("product/varients/values/<int:id>/", views.varients_values_manage, name="varients_values_manage"),
    path("product/varients/values/combination/<int:id>/", views.varients_values_combination, name="varients_values_combination"),
    path("product/generate_varients/<int:id>/", views.generate_varients, name="generate_varients"),
    # path("add_product/", views.add_product, name="add_product"),

    path("product_varients/", views.product_varients, name="product_varients"),
    path("varient_values/<int:id>/", views.varient_values, name="varient_values"),
    path('logout/', views.admin_logout, name='logout'),

]
