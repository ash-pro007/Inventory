from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page,  name="login"),
    path('login_page', views.login_page,  name="login_page"),
    path('signup', views.signup, name="signup"),

    path('login_page/logout_user', views.logout_user, name="logout_user"), 
    path('logout_user', views.logout_user, name="logout_user"), 

    path('home', views.home, name="home"),
    path('login_page/home', views.home, name="home"), 
    path('register_user', views.register_user, name="register_user"),
    path('login_user', views.login_user, name="login_user"),

    path('upload/', views.upload_file, name='upload_file'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('login_page/upload_file', views.upload_file, name='upload_file'),

    path('search_product', views.search_product, name='search_product'),

    path('login_page/search_product', views.search_product, name='search_product'),

    
    path('search_by_quantity', views.search_by_quantity, name='search_by_quantity'),
    path('login_page/search_by_quantity', views.search_by_quantity, name='search_by_quantity'),

    path('login_page/add_inventory', views.add_inventory, name='add_inventory'),
    path('login_page/add_product', views.add_product, name='add_product'),
    path('login_page/add_product_in_inventory', views.add_product_in_inventory, name='add_product_in_inventory'),

    path('login_page/reset_database', views.reset_database, name='reset_database')


    
]
 