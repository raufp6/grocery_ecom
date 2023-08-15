from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("account/",views.account, name="account"),
    
    path("address/",views.address, name="address"),
    path("address/add/",views.add_address, name="add_address"),
    path("address/edit/<int:id>/",views.edit_address, name="edit_address"),
    path("address/delete/<int:id>/",views.delete_address, name="delete_address"),

    path("orders/",views.orders, name="orders"),
    path("order/view/<int:id>/",views.order_details, name="order_details"),
    path("order/cancel_order/<int:id>/",views.cancel_order, name="cancel_order"),
    path("order/cancel_order_item/<int:id>/",views.cancel_order_item, name="cancel_order_item"),
    path("order/cancel_order_status/<int:id>/",views.cancel_order_status, name="cancel_order_status"),
    
    path("profile/",views.profile, name="profile"),

    path("accounts/password_change/",views.password_change, name="password_change"),

    path("wallet/",views.wallet, name="wallet"),
    
    
]