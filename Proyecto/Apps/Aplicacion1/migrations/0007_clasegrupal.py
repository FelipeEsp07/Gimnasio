# Generated by Django 5.1.7 on 2025-03-31 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion1', '0006_usuario_qr_code_accesslog'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaseGrupal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('dia', models.CharField(choices=[('LU', 'Lunes'), ('MA', 'Martes'), ('MI', 'Miércoles'), ('JU', 'Jueves'), ('VI', 'Viernes'), ('SA', 'Sábado'), ('DO', 'Domingo')], help_text='Día en que se dicta la clase', max_length=2)),
                ('hora', models.TimeField(help_text='Hora de inicio de la clase')),
                ('cupo_maximo', models.PositiveIntegerField(help_text='Número máximo de asistentes')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('instructor', models.ForeignKey(blank=True, help_text='Entrenador encargado de la clase', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Aplicacion1.empleado')),
            ],
        ),
    ]
