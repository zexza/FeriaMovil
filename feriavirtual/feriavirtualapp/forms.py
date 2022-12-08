from django import forms
from django.contrib.auth.forms import UserCreationForm
from requests import post
from .models import *
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm, TextInput, EmailInput
PRODUCTOS =(
    ("1", "Cerezas "),
    ("2", "Uvas"),
    ("3", "Arándanos "),
    ("4", "Nueces"),
    ("5", "Manzana"),
    ("6", "Ciruela"),
    ("7", "Peras"),
    ("9", "Durazno"),
    ("11", "Frutilla"),
    ("12", "Granada"),
    ("13", "Limón"),
    ("14", "Mandarina"),
    ("15", "Naranja"),
    ("16", "Sandia "),
    ("17", "Melón"),
    ("18", "Mora"),
    ("19", "Pera"),
    ("20", "Manzana"),
)
class FormRegistroUsuario(UserCreationForm):

    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','dni','email','password1','password2','rol','direccion','codigopostal']
        help_texts = {k:"" for k in fields}
class FormRegistroInterno(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','dni','email','password1','password2','direccion','codigopostal']
        help_texts = {k:"" for k in fields}
        


class FormPujarSubasta(forms.Form):
    cantidad = forms.IntegerField(help_text="Ingrese la cantidad que desea aportar para satisfacer el pedido.")

class FormProductos(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('producto','variedad','calibre','cantidad','precio', 'imagen',)
        labels = {
            'cantidad': ('Cantidad en cajas:'),
        }
class FormContratos(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(FormContratos, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(rol="1")  | User.objects.filter(rol="1")
    class Meta:
        model = Contrato
        fields = ('usuario','fecha_inicio','fecha_termino')

class FormVenta(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(FormVenta, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = User.objects.filter(rol="3")  | User.objects.filter(rol="2")
    class Meta:
        model = Post
        fields = ('cliente','productoreq','variedad','calibre','cantidad_necesaria','refrigeracion','contenido', 'imagen',)
        labels = {
            'cantidad_necesaria': ('Cantidad en cajas:'),
            'imagen': ('Imagen de referencia (opcional)')
        }
    def __init__(self, *args, **kwargs):
        super(FormVenta, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False
        self.fields['cliente'].queryset = User.objects.filter(rol="3")  | User.objects.filter(rol="2")
        self.fields['productoreq'].choices = PRODUCTOS
class FormVentaCliente(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('productoreq','variedad','calibre','cantidad_necesaria','refrigeracion','contenido', 'imagen',)
        labels = {
            'cantidad_necesaria': ('Cantidad en cajas:'),
            'imagen': ('Imagen de referencia (opcional)'),
            'productoreq': ('Producto requerido')
        }
    def __init__(self, *args, **kwargs):
        super(FormVentaCliente, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False



class FormSolicitudEstadoTransportista(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['EstadoSolicitud'].choices = [
                ("11", "En camino"),
                ("12", "Viaje interrumpido"),
                ("13", "Destino"),
            ]
    class Meta:
        model = Post
        fields = ('EstadoSolicitud',)
class FormSolicitudEstadoRevisor(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['EstadoSolicitud'].choices = [
                ("9", "Rechazar"),
                ("10", "Aprobar"),
            ]
    class Meta:
        model = Post
        fields = ('EstadoSolicitud',)
class FormSolicitudEstadoProductor(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['EstadoSolicitud'].choices = [
                ("6", "Entregado en bodega"),
                ("7", "Viaje Interrumpido")

            ]
    class Meta:
        model = Post
        fields = ('EstadoSolicitud',)    
class FormSolicitudClienteExterno(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['EstadoSolicitud'].choices = [
                ("14", "Pagar"),
                ("15", "Rechazar pedido"),

            ]
    class Meta:
        model = Post
        fields = ('EstadoSolicitud',)    
class FormSolicitudEstado(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['EstadoSolicitud'].choices = [
                ("1", "Aprobado"),
                ("2", "Rechazado"),
                ("3", "Pendiente")
            ]
    class Meta:
        model =  Post
        fields = ('EstadoSolicitud',)



class FormRegistrarTransporte(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ('tamaño','refrigeracion','tarifa',)
        
        
class FormEstadoSolicitud(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'EstadoSolicitud',)
        labels = {
            'EstadoSolicitud': ('Selecciones el estado :'),
        }
