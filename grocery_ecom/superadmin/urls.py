from django.urls import path
from superadmin import views

app_name = "superadmin"

urlpatterns = [
    path("",views.admin_login,name="login"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("category_list",views.category_list,name="category_list"),
    path('logout',views.admin_logout,name='logout'),

]