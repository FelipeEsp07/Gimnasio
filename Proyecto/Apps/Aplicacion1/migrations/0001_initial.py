# Generated by Django 5.1.7 on 2025-03-27 20:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=15)),
                ('direccion', models.TextField()),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('contraseña', models.CharField(max_length=128)),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='fotos_perfil/')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('aceptar_condiciones', models.BooleanField(default=False)),
                ('rol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Aplicacion1.rol')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puesto', models.CharField(max_length=100)),
                ('certificaciones', models.FileField(blank=True, null=True, upload_to='certificaciones/')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion1.usuario')),
            ],
        ),
    ]
