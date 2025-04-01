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
def test_acceso_usuario_view_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(username="usuario", password="pass123")
    client.login(username="usuario", password="pass123")
    
    url = reverse("acceso_usuario")
    response = client.get(url)
    assert response.status_code == 200
    assert any("acceso_usuario.html" in t.name for t in response.templates)

@pytest.mark.django_db
def test_dashboard_admin_view_authenticated(client, django_user_model):
    user = django_user_model.objects.create_superuser(username="admin", password="adminpass")
    client.login(username="admin", password="adminpass")
    
    url = reverse("dashboard_admin")
    response = client.get(url)
    assert response.status_code == 200
    assert any("dash_admin.html" in t.name for t in response.templates)

@pytest.mark.django_db
def test_dashboard_cliente_view_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(username="cliente", password="pass123")
    client.login(username="cliente", password="pass123")
    
    url = reverse("dashboard_cliente")
    response = client.get(url)
    assert response.status_code == 200
    assert any("dash_cliente.html" in t.name for t in response.templates)

@pytest.mark.django_db
def test_dashboard_entrenador_view_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(username="entrenador", password="pass123")
    client.login(username="entrenador", password="pass123")
    
    url = reverse("dashboard_entrenador")
    response = client.get(url)
    assert response.status_code == 200
    assert any("dash_entrenador.html" in t.name for t in response.templates)

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
