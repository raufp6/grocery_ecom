from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("login/",views.user_login, name="login"),
    path("sign-up/",views.register_view, name="sign-up"),
    path("verify_otp/",views.verify_otp, name='verify_otp'),

    # path("accounts/password_change/",views.password_change, name="password_change"),
    # path("accounts/password_change/done/",views.forgot_password, name="password_change_done"),
    path("accounts/password_reset/",views.password_reset, name="password_reset"),
    # path("accounts/password_reset/done/",views.forgot_password, name="password_reset_done"),
    # path("accounts/reset/<uidb64>/<token>/",views.forgot_password, name="password_reset_confirm"),
    # path("accounts/reset/done/",views.forgot_password, name="password_reset_complete"),
    

    path("logout/",views.user_logout, name='logout'),
]