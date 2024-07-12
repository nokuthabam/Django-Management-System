from django.urls import path, include, re_path
from . import views

app_name = 'management_app'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('logout/', views.user_logout, name='logout'),

]
