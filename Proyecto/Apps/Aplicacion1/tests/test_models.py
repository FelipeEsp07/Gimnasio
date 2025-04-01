
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto.settings') 
django.setup()

import pytest
from datetime import date, timedelta
from Apps.Aplicacion1.models import Rol, Usuario, ClaseGrupal

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
