from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("login/",views.user_login, name="login"),
    path("sign-up/",views.register_view, name="sign-up"),
    path("verify_otp/",views.verify_otp, name='verify_otp'),
    path("send_otp/<str:email>/",views.send_otp, name='send_otp'),


    path("send_otp_for_reset/<str:email>/",views.send_otp_for_reset, name='send_otp_for_reset'),
    # path("accounts/password_change/",views.password_change, name="password_change"),
    # path("accounts/password_change/done/",views.forgot_password, name="password_change_done"),
    path("accounts/password_reset/",views.password_reset, name="password_reset"),
    path("verify_otp_reset/",views.verify_otp_reset, name='verify_otp_reset'),
    path("change_password/",views.change_password, name='change_password'),
    # path("accounts/password_reset/done/",views.forgot_password, name="password_reset_done"),
    # path("accounts/reset/<uidb64>/<token>/",views.forgot_password, name="password_reset_confirm"),
    # path("accounts/reset/done/",views.forgot_password, name="password_reset_complete"),
    

    path("logout/",views.user_logout, name='logout'),
]