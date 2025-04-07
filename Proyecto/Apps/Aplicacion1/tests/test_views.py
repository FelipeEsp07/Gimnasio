import os
import django
import pytest
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto.settings')
django.setup()

@pytest.mark.django_db
def test_home_view(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assert any("home.html" in t.name for t in response.templates)

@pytest.mark.django_db
def test_dashboard_admin_view_authenticated(client, django_user_model):
    user = django_user_model.objects.create_superuser(username="admin", password="adminpass")
    client.login(username="admin", password="adminpass")
    
    url = reverse("dashboard_admin")
    response = client.get(url)
    assert response.status_code == 200
    assert any("dash_admin.html" in t.name for t in response.templates)

@pytest.mark.django_db
def test_login_clientes_view(client):
    url = reverse("login_clientes")
    response = client.get(url)
    assert response.status_code == 200
    assert any("login_clientes.html" in t.name for t in response.templates)

@pytest.mark.django_db
def test_reg_clientes_view(client):
    url = reverse("reg_clientes")
    response = client.get(url)
    assert response.status_code == 200
    assert any("reg_clientes.html" in t.name for t in response.templates)
