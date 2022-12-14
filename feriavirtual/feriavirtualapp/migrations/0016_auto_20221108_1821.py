# Generated by Django 3.0.6 on 2022-11-08 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feriavirtualapp', '0015_auto_20221108_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='EstadoSolicitud',
            field=models.CharField(choices=[('1', 'Aprobado'), ('2', 'Rechazado'), ('3', 'Pendiente'), ('4', 'Subasta de transporte'), ('6', 'Entregado en bodega'), ('7', 'Revision de calidad'), ('8', 'Rechazado en revision'), ('9', 'Revisado'), ('10', 'En camino'), ('11', 'Viaje interrumpido'), ('12', 'Destino'), ('13', 'Aceptado por el destinatario'), ('14', 'Rechazado por el destinatario'), ('15', 'Saldo')], default='3', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='posthistorico',
            name='EstadoSolicitud',
            field=models.CharField(choices=[('1', 'Aprobado'), ('2', 'Rechazado'), ('3', 'Pendiente'), ('4', 'Subasta de transporte'), ('6', 'Entregado en bodega'), ('7', 'Revision de calidad'), ('8', 'Rechazado en revision'), ('9', 'Revisado'), ('10', 'En camino'), ('11', 'Viaje interrumpido'), ('12', 'Destino'), ('13', 'Aceptado por el destinatario'), ('14', 'Rechazado por el destinatario'), ('15', 'Saldo')], default='3', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='posthistorico',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ClienteSolih', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='posthistorico',
            name='comentariosTransportista',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='posthistorico',
            name='contenido',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='posthistorico',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='posthistorico',
            name='refrigeracion',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
