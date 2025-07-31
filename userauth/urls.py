from django.urls import path
from .import views

app_name = 'userauth'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('cab/', views.user_cab, name='cab'),
    path('logout/', views.user_logout, name = 'logout'),
    path('edit/', views.user_edit, name = 'edit'),
    path('change_pass/', views.change_pass, name = 'change_pass'),
]