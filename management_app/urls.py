from django.urls import path, include, re_path
from . import views

app_name = 'management_app'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('logout/', views.user_logout, name='logout'),
    path('course_list/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

]
