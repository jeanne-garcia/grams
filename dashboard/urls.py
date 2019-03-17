from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogIn, name='login-placeholder'),
    path('home/', views.Dashboard, name='dashboard'),
]
