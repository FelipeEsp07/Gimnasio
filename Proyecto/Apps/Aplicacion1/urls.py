from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('inicio/', views.inicio, name='inicio'),
    path('crear_rol/', views.crear_rol, name='crear_rol'),
    path('eliminar_rol/<int:id>/', views.eliminar_rol, name='eliminar_rol'),
    path('reg_clientes/', views.reg_clientes, name='reg_clientes'),
    path('reg_empleados/', views.reg_empleados, name='reg_empleados'),
    path('login_clientes/', views.login_clientes, name='login_clientes'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('eliminar_empleado/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('editar_empleado/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('registrar_plan_membresia/', views.registrar_plan_membresia, name='registrar_plan_membresia'),
    path('editar_plan/<int:id>/', views.editar_plan, name='editar_plan'),
    path('eliminar_plan/<int:id>/', views.eliminar_plan, name='eliminar_plan'),
    path('registrar_equipo/', views.registrar_equipo, name='registrar_equipo'),
    path('eliminar_equipo/<int:id>/', views.eliminar_equipo, name='eliminar_equipo'),
    path('editar_equipo/<int:id>/', views.editar_equipo, name='editar_equipo'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

