from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("account/",views.account, name="account"),
    path("address/",views.address, name="address"),
    path("orders/",views.orders, name="orders"),
    path("profile/",views.profile, name="profile"),
    path("address/add/",views.add_address, name="add_address"),
    path("address/edit/<int:id>",views.edit_address, name="edit_address"),
    path("address/delete/<int:id>",views.delete_address, name="delete_address"),
]