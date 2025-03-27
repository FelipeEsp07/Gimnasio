from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inicio/', views.inicio, name='inicio'),
    path('reg_clientes/', views.reg_clientes, name='reg_clientes'),
    path('reg_empleados/', views.reg_empleados, name='reg_empleados'),
    path('login_clientes/', views.login_clientes, name='login_clientes'),
]

