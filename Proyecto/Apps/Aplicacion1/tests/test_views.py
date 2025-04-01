import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto.settings') 
django.setup()

import pytest
from django.urls import reverse
from Apps.Aplicacion1.models import PlanMembresia
@pytest.mark.django_db
def test_home_view(client):
    PlanMembresia.objects.create(
        nombre="Plan Básico",
        descripcion="Acceso básico",
        precio=10.00,
        duracion_meses=1,
    )
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assert "Plan Básico" in response.content.decode()
