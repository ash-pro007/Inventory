from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page,  name="login"),
    path('login_page', views.login_page,  name="login_page"),
    path('signup', views.signup, name="signup"),
    path('home', views.home, name="home"),
    path('login_page/home', views.home, name="home"), 
    path('register_user', views.register_user, name="register_user"),
    path('login_user', views.login_user, name="login_user"),

    path('upload/', views.upload_file, name='upload_file'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('login_page/upload_file', views.upload_file, name='upload_file'),
    
]
 