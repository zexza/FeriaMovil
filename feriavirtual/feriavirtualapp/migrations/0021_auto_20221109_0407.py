# Generated by Django 3.0.6 on 2022-11-09 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feriavirtualapp', '0020_auto_20221108_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Saldo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='EstadoSolicitud',
            field=models.CharField(choices=[('1', 'Aprobado'), ('2', 'Rechazado'), ('3', 'Pendiente'), ('4', 'Subasta de transporte'), ('5', 'Transporte Listo'), ('6', 'Entregado en bodega'), ('7', 'Viaje interrumpido (productor)'), ('8', 'Revision de calidad'), ('9', 'Rechazado en revision'), ('10', 'Revisado'), ('11', 'En camino'), ('12', 'Viaje interrumpido (transportista)'), ('13', 'Destino'), ('14', 'Aceptado por el destinatario'), ('15', 'Rechazado por el destinatario'), ('16', 'Saldo')], default='3', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='posthistorico',
            name='EstadoSolicitud',
            field=models.CharField(choices=[('1', 'Aprobado'), ('2', 'Rechazado'), ('3', 'Pendiente'), ('4', 'Subasta de transporte'), ('5', 'Transporte Listo'), ('6', 'Entregado en bodega'), ('7', 'Viaje interrumpido (productor)'), ('8', 'Revision de calidad'), ('9', 'Rechazado en revision'), ('10', 'Revisado'), ('11', 'En camino'), ('12', 'Viaje interrumpido (transportista)'), ('13', 'Destino'), ('14', 'Aceptado por el destinatario'), ('15', 'Rechazado por el destinatario'), ('16', 'Saldo')], default='3', max_length=50, null=True),
        ),
    ]
