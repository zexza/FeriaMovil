from django.urls import path , include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
urlpatterns = [
    path('lista-contratos/', views.listaContratos, name='listaContratos'),
    path('gestion-contratos/', views.gestionContratos, name='gestionContratos'),
    path('contratos/', views.contratos, name='contratos'),
    path('register/', views.register, name='register'),
    path('registerinterno/', views.registerinterno, name='register-interno'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    
    path('pagar/<int:total>/<int:pk>', views.pagar, name="pagar"),
 
    path('seguimiento/<int:pk>/', views.seguimiento, name="seguimiento"),
    path('seguimientoLista/', views.seguimientoLista, name='seguimientoLista'),
    path('seguimientoDetalle/<int:pk>/', views.seguimientoDetalle, name='seguimientoDetalle'),

    
    
    path('ingresar-productos/', views.ingresarproductos, name='ingresar-productos'),
    path('mis-productos/', views.misproductos, name='mis-productos'),
    
    
    path('venta/', views.venta, name='venta'),
    
    #path('subasta/<int:pk>/', views.subasta, name='subasta'),
    
    #path('pagarsubasta/<int:pk>/', views.pagarsubasta, name='pagarsubasta'),
    path('terminar/<int:pk>/', views.terminar, name='terminar'),
    path('terminarsaldo/', views.webpaycommit, name='terminarsaldo'),
    #path('pagar/<int:total>/<int:pk>', views.pagar, name='pagar'),
    path('pagar/', views.pagar, name='pagar'),
    
    path('Solicitud/', views.Solicitud, name='Solicitud'),
    path('Solicitudes/', views.solicitudes, name='Solicitudes'),
    path('modificarsoli/<int:pk>/', views.modificarSolicitud, name="modificarSolicitud"),

    path('registrarTransporte/', views.registrarTransporte, name="registrarTransporte"),
    path('transportesRegistrados/', views.transportesRegistrados, name="transportesRegistrados"),

    path('Venta-local/', views.Ventalocal, name="Ventalocal"),
    
    
    path('add_product_carrito/<int:product_id>/', add_product_carrito, name='add_product_carrito'),
    path('add_product_catalogo/<int:product_id>/', add_product_catalogo, name='add_product_catalogo'),
    path('remove_product/<int:product_id>/', remove_product, name='remove_product'),
    path('decrement_product/<int:product_id>/', decrement_product, name='decrement_product'),
    path('clear/', clear_cart, name='clear_cart'),
    path('carrito.html', views.webpay),

    path('solicitudClientes/', views.solicitudClientes, name="solicitudClientes"),

    path('solicitudesTransportista/', views.solicitudesTransportista, name="solicitudesTransportista"),
    path('modificarSolicitudTransportista/<int:pk>/', views.modificarSolicitudTransportista, name="modificarSolicitudTransportista"),

    path('solicitudesRevisor/', views.solicitudesRevisor, name="solicitudesRevisor"),
    path('modificarSolicitudRevisor/<int:pk>/', views.modificarSolicitudRevisor, name="modificarSolicitudRevisor"),

    path('solicitudesProductor/', views.solicitudesProductor, name="solicitudesProductor"),
    path('modificarsolicitudProductor/<int:pk>/', views.modificarSolicitudProductor, name="modificarsolicitudProductor"),

    path('solicitudesClienteExterno/', views.solicitudesClienteExterno, name="solicitudesClienteExterno"),
    path('modificarSolicitudClienteExterno/<int:pk>/', views.modificarSolicitudClienteExterno, name="modificarSolicitudClienteExterno"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
