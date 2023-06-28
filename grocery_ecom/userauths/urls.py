from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("login/",views.user_login, name="login"),
    path("sign-up/",views.register_view, name="sign-up"),
    path("verify_otp/",views.verify_otp, name='verify_otp'),
    path("logout/",views.user_logout, name='logout'),
]