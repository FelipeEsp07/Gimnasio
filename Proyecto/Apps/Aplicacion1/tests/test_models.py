import os
import django
from datetime import date, timedelta
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto.settings') 
django.setup()

from Apps.Aplicacion1.models import Rol, Usuario, Empleado, PlanMembresia, Equipo, AccessLog, ClaseGrupal

@pytest.mark.django_db
def test_rol_str():
    rol = Rol.objects.create(nombre="Dueño")
    assert str(rol) == "Dueño"

@pytest.mark.django_db
def test_usuario_str():
    usuario = Usuario.objects.create(
        nombre="Esteban",
        cedula="123456789",
        telefono="3204875496",
        direccion="Carrera 10 # 20 - 30",
        correo="esteban@gmail.com",
        contraseña="contraseña",
        aceptar_condiciones=True,
    )
    assert str(usuario) == "Esteban"

@pytest.mark.django_db
def test_empleado_str():
    usuario = Usuario.objects.create(
        nombre="Ana",
        cedula="987654321",
        telefono="3216549870",
        direccion="Calle 45 # 12 - 89",
        correo="ana@example.com",
        contraseña="segura123",
        aceptar_condiciones=True,
    )
    empleado = Empleado.objects.create(usuario=usuario, puesto="Entrenador Personal")
    assert str(empleado) == "Ana - Entrenador Personal"

@pytest.mark.django_db
def test_plan_membresia_str():
    plan = PlanMembresia.objects.create(
        nombre="Plan Premium",
        descripcion="Acceso a todas las instalaciones y clases grupales.",
        precio=50.00,
        duracion_meses=3
    )
    assert str(plan) == "Plan Premium"

@pytest.mark.django_db
def test_equipo_str():
    equipo = Equipo.objects.create(
        nombre="Bicicleta Estática",
        tipo="Cardio",
        estado="DISP",
        cantidad=5
    )
    assert str(equipo) == "Bicicleta Estática (Disponible)"

@pytest.mark.django_db
def test_access_log_str():
    usuario = Usuario.objects.create(
        nombre="Pedro",
        cedula="456789123",
        telefono="1234567890",
        direccion="Avenida 9 # 14 - 50",
        correo="pedro@example.com",
        contraseña="password",
        aceptar_condiciones=True,
    )
    access_log = AccessLog.objects.create(
        usuario=usuario,
        correo=usuario.correo,
        ip_address="192.168.1.1"
    )
    assert "Acceso de Pedro el" in str(access_log)

@pytest.mark.django_db
def test_clase_grupal_get_next_date():
    clase = ClaseGrupal.objects.create(
        nombre="Clase de Yoga",
        descripcion="Clase de yoga para principiantes",
        dia="LU",
        hora="10:00",
        cupo_maximo=20,
    )
    next_date = clase.get_next_date()
    today = date.today()
    monday = 0 
    days_ahead = monday - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    expected_date = today + timedelta(days=days_ahead)
    assert next_date == expected_date
