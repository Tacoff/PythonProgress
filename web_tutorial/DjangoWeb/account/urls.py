from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"
urlpatterns = [
    # path('login/', views.user_login, name="user_login"),
    path('login/', auth_views.login, name="user_login"),
    path('new_login/', auth_views.login, {"template_name": "account/login.html"}),
    # path('logout/', auth_views.logout, name="user_logout"),
    path('logout/', auth_views.logout, {"template_name": "account/logged_out.html"}, name="user_logout"),
    path('register/', views.register, name="user_register"),
    path('password-change/', auth_views.password_change, {"post_change_redirect": "account/password-change-done.html"},
         name="password_change"),
    path('password-change-done/', auth_views.password_change_done, name="password_change_done"),
]