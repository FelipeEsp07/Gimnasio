from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
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
    path('acceso/<str:token>/', views.registrar_acceso, name='registrar_acceso'),
    path('dashboard_entrenador/', views.dashboard_entrenador, name='dashboard_entrenador'),
    path('registrar_clase_grupal/', views.registrar_clase_grupal, name='registrar_clase_grupal'),
    path('editar_clase_grupal/<int:id>/', views.editar_clase_grupal, name='editar_clase_grupal'),
    path('eliminar_clase_grupal/<int:id>/', views.eliminar_clase_grupal, name='eliminar_clase_grupal'),
    path('dashboard_cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('acceso_usaurio/', views.acceso_usuario, name='acceso_usuario'),
    path('descargar_qr/', views.descargar_qr, name='descargar_qr'),
    path('editar_cliente/', views.editar_cliente, name='editar_cliente'),
    path('inscribir_clase/<int:clase_id>/', views.inscribir_a_clase, name='inscribir_clase'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

