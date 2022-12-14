# Generated by Django 3.0.6 on 2022-11-06 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feriavirtualapp', '0005_auto_20221103_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Codigopostal',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='Direccion',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='EstadoSolicitud',
            field=models.CharField(choices=[('1', 'Aprobado'), ('2', 'Rechazado'), ('3', 'Pendiente'), ('4', 'Subasta Transporte'), ('5', 'Esperando productos en bodega central'), ('6', 'Revision de calidad'), ('7', 'En camino'), ('8', 'Destino'), ('9', 'Saldo')], default='3', max_length=50, null=True),
        ),
    ]
