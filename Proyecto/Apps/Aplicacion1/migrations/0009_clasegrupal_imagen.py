# Generated by Django 5.1.7 on 2025-03-31 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion1', '0008_alter_clasegrupal_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasegrupal',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='clases_grupales/'),
        ),
    ]
