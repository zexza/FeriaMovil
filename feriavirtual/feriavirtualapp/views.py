from ast import Try
from datetime import datetime
import operator
from django.db.models.aggregates import Count
from django.db.models.expressions import Exists
from django.shortcuts import render
from django.utils import timezone
from requests import post
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.error.transbank_error import TransbankError
from django.contrib.auth import login
from operator import attrgetter, itemgetter
from django.core.mail import send_mail
from .cart import Cart
from .context_processor import cart_total_amount
from django.views.decorators.csrf import csrf_protect
from dash import Dash, dcc, html, Input, Output
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_xhtml2pdf.utils import generate_pdf
from django.db.models import Q
from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse
import math
from django.conf import settings
from django.template.loader import get_template

import os

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pyodbc
import json
import pdfkit




def ComprobantePDF(request,pk):
    config_path = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=config_path)
    
    template_path = 'my_template.html'
    template = get_template(template_path)
    
    soli = Post.objects.get(pk=pk)
    Producto = []
    subtotal=0
    for p in soli.producto.all():
        print()
        postP = Post_productos.objects.get(producto=p, post=soli)
        Producto.append([p,postP.cantidad_pujada])

        subtotal = subtotal + postP.cantidad_pujada*p.precio
    impuesto= subtotal*0.03
    total = subtotal+impuesto
    subtotal=str('{:,.0f}'.format(subtotal).replace(",", "@").replace(".", ",").replace("@", "."))
    impuesto=str('{:,.0f}'.format(impuesto).replace(",", "@").replace(".", ",").replace("@", "."))
    total=str('{:,.0f}'.format(total).replace(",", "@").replace(".", ",").replace("@", "."))
    
    context = {'debug': settings.DEBUG,'total':total,'impuesto':impuesto,'subtotal':subtotal,'Producto':Producto,'postP':postP,'soli':soli,}
    
    html = template.render(context)

    pdf = pdfkit.from_string(html, configuration = config)


    # Generate download
    pdf_path = os.path.join(settings.BASE_DIR, 'static')
    response = HttpResponse(pdf, content_type='application/pdf',  )

    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    # print(response.status_code)
    if response.status_code != 200:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



    



a=1
a=1
# Create your views here.

def index(request):
    cart = Cart(request)
    return render(request, 'index.html', {})
def listaContratos(request):
    cart = Cart(request)
    cont = Contrato.objects.all()
    context ={'cont':cont}
    return render(request, 'lista-contratos.html', context)
def gestionContratos(request):
    cart = Cart(request)
    return render(request, 'gestion-contratos.html', {})
def contratos(request):
    cart = Cart(request)    
    if request.method == 'POST':
        form = FormContratos(request.POST)
        if form.is_valid():
            cont = form.save(commit=False)
            cont.username = form.cleaned_data['usuario']
            existeuser = get_object_or_404(User, username=cont.username)
           
            
            if Contrato.objects.filter(usuario=existeuser, vigencia=True):
                messages.error(request, f'Este usuario ya tiene un contrato vigente.')
            else:  
                cont.fecha_inicio = form.cleaned_data['fecha_inicio']
                cont.fecha_termino = form.cleaned_data['fecha_termino']
                if cont.fecha_inicio > cont.fecha_termino:
                    messages.error(request, f'La fecha de inicio no puede ser mayor a la de termino del contrato')
                else:
                    cont.vigencia = True
                    form.save()
                    messages.success(request, f'Contrato para usuario {cont.username} creado')
                    return redirect('contratos')
    else:
        form = FormContratos()
    context = { 'form': form }
    return render(request, 'contratos.html', context)

def register(request):
    cart = Cart(request)    
    if request.method == 'POST':
        form = FormRegistroUsuario(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if form.rol == "6":
                form.is_staff = True
            

            form.save()
            messages.success(request, f'Usuario {form.username} creado')
            return redirect('/register')
    else:
        form = FormRegistroUsuario()
    context = { 'form': form }
    return render(request, 'register.html',context)
def registerinterno(request):
    cart = Cart(request)    
    if request.method == 'POST':
        form = FormRegistroInterno(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('login')
    else:
        form = FormRegistroInterno()
    context = { 'form': form }
    return render(request, 'register-interno.html',context)    


def seguimientoDetalle(request,pk):
    cart = Cart(request)    
    solis = Posthistorico.objects.filter(idpost=pk)
    print(solis)
    context = {'solis':solis}
    return render(request, 'seguimientoDetalle.html',context)




def seguimiento(request,pk):
    cart = Cart(request)        
    if request.user.is_staff:
        solis = Post.objects.filter(pk=pk)
    elif request.user.rol =="1" or request.user.rol =="5" or request.user.rol =="3" or request.user.rol =="2" or request.user.rol =="6":
        solis = Post.objects.filter(pk=pk)
    else:
        solis = Post.objects.filter(usuario=request.user,pk=pk)
    context = {'solis':solis}
    return render(request, 'seguimiento.html',context)

def seguimientoLista(request):
    user= request.user
    cart = Cart(request)
    solis = []
    prof = []
    if request.user.is_staff:
        solis = Post.objects.all()
    elif request.user.rol =="5":
         solis = Post.objects.all()
    elif request.user.rol =="6":
         solis = Post.objects.all()
    elif request.user.rol =="1":
        post = Post.objects.all()
        print(post)
        for p in post:

            for prod in p.producto.filter(autor=user):
                print(prod)
                postprod = Post_productos.objects.get(post=p, producto=prod)
                s = Post.objects.get(pk=postprod.post.pk)
                solis.append(s)



    elif request.user.rol =="2" or request.user.rol =="3":
        solis = Post.objects.filter(cliente=user)
    else:
        solis = Post.objects.filter(usuario=request.user)
    context = {'solis':solis}
    return render(request, 'seguimientoLista.html',context)



def comprobante(request,pk):
    cart = Cart(request)        
    soli = Post.objects.get(pk=pk)
    soliF = Post.objects.get(pk=pk)
    Producto = []
    subtotal=0
    for p in soli.producto.all():
        print()
        postP = Post_productos.objects.get(producto=p, post=soli)
        Producto.append([p,postP.cantidad_pujada])

        subtotal = subtotal + postP.cantidad_pujada*p.precio 
        
    subtotal = subtotal + soli.transporte.tarifa
    impuesto= subtotal*0.03
    total = subtotal+impuesto
    subtotal=str('{:,.0f}'.format(subtotal).replace(",", "@").replace(".", ",").replace("@", "."))
    impuesto=str('{:,.0f}'.format(impuesto).replace(",", "@").replace(".", ",").replace("@", "."))
    total=str('{:,.0f}'.format(total).replace(",", "@").replace(".", ",").replace("@", "."))
    
    context = {'total':total,'impuesto':impuesto,'subtotal':subtotal,'Producto':Producto,'postP':postP,'soli':soli,}
    
    
    return render(request, 'comprobante.html',context)






def seguimientoComprobante(request):
    user= request.user
    cart = Cart(request)
    if request.user.rol =="5":
        solis = Post.objects.filter(EstadoSolicitud= '17')
    else:
        solis = Post.objects.filter(cliente=user,EstadoSolicitud= '17')
    context = {'solis':solis}
    return render(request, 'seguimientoComprobante.html',context)


app = Dash(__name__)

@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))

class DTEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is datetime object
        # convert it to a string
        if isinstance(obj, datetime):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
    
    
    
    
    
         #langs = Fecha
     #students = usuario
    
    
     #x =langs ,
         #y = students,



def ingresarproductos(request):
    cart = Cart(request)    
    if request.method == 'POST':
        form = FormProductos(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.autor = request.user
            form.save()
            messages.success(request, f'Productos agregados a tu lista de productos')
            return redirect('mis-productos')
            
    else:
        form = FormProductos()
    context = { 'form': form }
    return render(request, 'ingresar-productos.html',context)




def connection(request):
    s = '186.78.254.17\DESKTOP-A7GEGG2\SQL2019TAB,14334' #Your server name 
    d = 'sqlite8' #name bd  
    u = 'sa' #Your login
    p = 'Pvsa**2021' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn 
    

def Consulta(request):
    Estado = 'Completada'
    solis = Post.objects.filter(EstadoSolicitud='17')
    if  request.method == 'POST'and 'completada' in request.POST:
        solis = Post.objects.filter(EstadoSolicitud='17')
        Estado = 'Completada'
    elif request.method == 'POST'and 'nocompletada' in request.POST:
        solis = Post.objects.filter(EstadoSolicitud__in=("11","13"))
        Estado = 'No Completada'
    print(solis)
    Producto = []
    subtotal=0
    tarifa =0
    PostCobro =[]

    for soli in solis:
        for p in soli.producto.all():
            postP = Post_productos.objects.get(producto=p, post=soli)
            Producto.append([p,postP])
            subtotal = subtotal + postP.cantidad_pujada*p.precio
            PostCobro.append([str(soli.pk), postP.producto.pk,postP.producto.autor, postP.cantidad_pujada, p.precio, postP.cantidad_pujada*p.precio ,soli.transporte.tarifa,])
        if soli.transporte:
            tarifa = tarifa + soli.transporte.tarifa
    Tarifaproductos=subtotal+tarifa
    impuesto= Tarifaproductos*0.03
    Cobro = Tarifaproductos+impuesto
    subtotal=str('{:,.0f}'.format(subtotal).replace(",", "@").replace(".", ",").replace("@", "."))
    impuesto=str('{:,.0f}'.format(impuesto).replace(",", "@").replace(".", ",").replace("@", "."))
    Cobro=str('{:,.0f}'.format(Cobro).replace(",", "@").replace(".", ",").replace("@", "."))
    Tarifaproductos=str('{:,.0f}'.format(Tarifaproductos).replace(",", "@").replace(".", ",").replace("@", "."))


    DataFramePostCobro = pd.DataFrame(PostCobro,columns=['PostPK','PkProducto','Productor','CantidadPujada','PrecioProducto','PrecioProductos','TarifaTrasporte'])
    print(DataFramePostCobro)
   


    DataframePost= pd.DataFrame(    DataFramePostCobro.groupby(['PostPK','TarifaTrasporte'])['PrecioProductos'].sum())
    
    DataframePost= pd.DataFrame(  DataframePost.reset_index() )
    
    DataframePost= pd.DataFrame(    DataFramePostCobro.groupby(['PostPK','TarifaTrasporte'])['PrecioProductos'].sum())
    
    DataframePost= pd.DataFrame(  DataframePost.reset_index() )
    
    Pagatarifatrasporte=DataframePost['TarifaTrasporte'] + DataframePost['PrecioProductos']
    DataframePost.insert(3, "Pagatarifatrasporte", Pagatarifatrasporte, True)
    
    CobroFinal =DataframePost['Pagatarifatrasporte'] *1.03
    DataframePost.insert(4, "CobroFinal", CobroFinal, True)
    
    Ganacias =DataframePost['Pagatarifatrasporte'] *0.03
    DataframePost.insert(5, "Ganacias", Ganacias, True)

    print(DataframePost)

    '''Graficos'''



    figGeneral = px.bar(DataframePost, x='PostPK',y='CobroFinal', color='PostPK',
        title="Solicitud / Cobro Final",
        
    )
    figGeneral.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    
    
    chartGeneral = figGeneral.to_html()




    figP = px.bar(DataframePost, x='PostPK',y='TarifaTrasporte', color='PostPK',
        title="Solicitud / Tarifa Trasporte",
        
    )
    figP.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chartP = figP.to_html()

    figProd = px.bar(DataframePost, x='PostPK',y='PrecioProductos', color='PostPK',
        title="Solicitud / Precio Productos",
       
    )
    figProd.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chartfigProd = figProd.to_html()
    
    fig = px.bar(DataframePost, x='PostPK',y='Ganacias', color='PostPK',
                title="Solicitud / Ganacias ",
               
    )
    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chart = fig.to_html()



    context = {'chart':chart,'chartfigProd':chartfigProd,'chartP':chartP,'chartGeneral':chartGeneral,'Tarifaproductos':Tarifaproductos,'Estado':Estado,'tarifa':tarifa,'Cobro':Cobro,'impuesto':impuesto,'subtotal':subtotal,'Producto':Producto}
    return render(request, 'Consulta.html',context)
        
    '''
    figUsuario = px.bar(DataframeConsulta, x='Transportista',
        title="Post/Transportista",
        labels={'Usuario': 'Usuario', 'Fecha': 'Fecha'}, color='Transportista',
    )
    figUsuario.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chartUsuario = figUsuario.to_html()
    
    
    
    df = pd.DataFrame(list(Post.objects.all().values()))
    fig = px.bar(DataframeConsulta, x='Usuario', color='Usuario',
                title="Post/Usuarios",
                labels={'Usuario': 'Usuario', 'Fecha': 'Fecha'},
    )
    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chart = fig.to_html()
    
    
    df = px.data.tips()
    labels = GrupbyProducto.index
    values = GrupbyProducto
    figP = go.Figure(data=[go.Pie(labels=labels, values=values)])
    
    
    figP.update_layout(
    title="Plot Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
    chartP = figP.to_html()
    context = { 'DataframeConsultaSumaProductortarifa':DataframeConsultaSumaProductortarifa,'DataframePost':DataframePost,'form': form ,'chart': chart,'chartP': chartP,'chartUsuario':chartUsuario,'DataframeConsultaSumaProductor':DataframeConsultaSumaProductor,'Df_grouPostIDPrecioFinalTotal':Df_grouPostIDPrecioFinalTotal,'Df_grouPostIDGananciaTotal':Df_grouPostIDGananciaTotal,'chartGeneral':chartGeneral}
        '''





def ingresarproductos(request):
    cart = Cart(request)    
    if request.method == 'POST':
        form = FormProductos(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.autor = request.user
            form.save()
            messages.success(request, f'Productos agregados a tu lista de productos')
            return redirect('mis-productos')
            
    else:
        form = FormProductos()
    context = { 'form': form }
    return render(request, 'ingresar-productos.html',context)

FormEstadoSolicitud

def misproductos(request):
    cart = Cart(request)
    prod = Producto.objects.filter(autor=request.user)
    context ={'prod':prod}
    return render(request, 'misproductos.html',context)
def venta(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = FormVenta(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.usuario = request.user
            form.fecha_creacion = timezone.now()
            form.save()
            messages.success(request, f'Venta iniciada!')
            return redirect('/')
    else:
        form = FormVenta()
    context = { 'form': form }
    return render(request, 'iniciar-venta.html',context)

def pagar(request,total,pk):
    cart = Cart(request)
    total = total   
    buy_order = str(pk)
    session_id = str(1)
    return_url = 'http://127.0.0.1:8000/terminar/'+str(pk)+'/'

    amount = total
    total= str('{:,.0f}'.format(total).replace(",", "@").replace(".", ",").replace("@", "."))
    try:
        response = Transaction().create(buy_order, session_id, amount, return_url)
        context ={'total':total,"response":response}
        print(amount)
        
        return render(request, 'pagar.html', context) 
    except TransbankError as e:
        print(e.message)
        print(e.message)
        error =e.message
        context ={'total':total,"error":error,}
        return render(request, 'pagar.html', context) 

def notificacion(request):
    cart = Cart(request)
    try:
        notis=Notificacion.objects.filter(usuario=request.user)
        messages.success(request, f'Tienes notificaciones de pago pendientes.')
        context={'notis':notis}
    except:
        messages.error(request, f'No tienes notificaciones actualmente.')
    context={'notis':notis}
    return render(request, 'notificacion.html',context) 

def terminar(request,pk):
    cart = Cart(request)
    token = request.GET.get("token_ws")
    try:
        response = Transaction().commit(token) 
        soli = Post.objects.get(pk=pk)
        soli.EstadoSolicitud = "17"
        soli.save()
        ccorreo= soli.cliente.email
        '''send_mail(
                'Su producto a sido completado, revise el comprobante de pago en http://127.0.0.1:8000/seguimientoComprobante/',
                'maipo_grande@gmail.com',
                [ccorreo],
                fail_silently=False,)
           '''                        
        #================COMPROBANTES DE PAGO==================
        #================PRODUCTORES==========================
        cantidadprods = len(soli.producto.all())
        cantidaddivida = soli.cantidad_actual//cantidadprods
        
        for p in soli.producto.all():

            postP = Post_productos.objects.get(producto=p, post=soli)

            comProd = Comprobante(usuario=p.autor,solicitud = soli,monto=p.precio * postP.cantidad_pujada)
            comProd.save()
            print(comProd)
        #================TRANSPORTISTA========================
        comTransp = Comprobante(usuario=soli.transporte.transportista,solicitud=soli,monto=soli.transporte.tarifa)
        comTransp.save()
        print(comTransp)

        messages.success(request, f'Pago realizado exitosamente.')
        return render(request, 'terminar.html',{"token": token,"response": response})
    except TransbankError as e:
        messages.error(request, f'Error en la transaccion de pago.')
        error =e.message
        print(e.message)
        print(token)
        return render(request, 'terminar.html', {"error":error})   

def Solicitud(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = FormVenta(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.usuario = request.user
            form.fecha_creacion = timezone.now()
            
            form.save()
            messages.success(request, f'Venta iniciada!')
            return redirect('/Solicitudes')
    else:
        form = FormVenta()
    context = { 'form': form }
    return render(request, 'Solicitud.html',context)
#SOLICITUD CLIENTES
def solicitudClientes(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = FormVentaCliente(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.usuario = request.user
            post.fecha_creacion = timezone.now()
            post.save()
            messages.success(request, f'Solicitud enviada')
            return redirect('/Solicitudes')
    else:
        form = FormVentaCliente()
    context = { 'form': form }
    return render(request, 'solicitudClientes.html',context)

def solicitudes(request):
    cart = Cart(request)
    solis = []
    soli = Post.objects.filter(EstadoSolicitud__in=("3","4","6","10"))
    for s in soli:
        if not s.transportista:
            solis.append(s)

    
    context ={'solis':solis}
    return render(request, 'Solicitudes.html', context)

def solicitudesTransportista(request):
    cart = Cart(request)
    solit = Post.objects.filter(transportista=request.user,EstadoSolicitud__in=("10","11","12","13","15"))
    context ={'solit':solit}
    return render(request, 'SolicitudesTransportista.html', context)

def solicitudesRevisor(request):
    cart = Cart(request)
    solir = Post.objects.filter(EstadoSolicitud__in=("6","8"))
    context ={'solir':solir}
    return render(request, 'solicitudesRevisor.html', context)
def solicitudesProductor(request):
    cart = Cart(request)
    post = Post.objects.filter(EstadoSolicitud__in=("1","4","5"))
    solip = []
    enbodega = False
    for p in post:
       
        for prod in p.producto.filter(autor=request.user):
            post_prod = Post_productos.objects.get(post=p, producto= prod)
            enbodega=post_prod.enbodega
            
            solip = Post.objects.filter(producto=prod)



    context ={'solip':solip,'enbodega':enbodega}
    
    return render(request, 'solicitudesProductor.html', context)
def solicitudesClienteExterno(request):
    cart = Cart(request)
    soli = Post.objects.filter(cliente=request.user,EstadoSolicitud__in=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"))

    context ={'soli':soli}
    return render(request, 'solicitudesClienteExterno.html', context)
def modificarSolicitud (request, pk):
    cart = Cart(request)
    SolicitudPK = Post.objects.get(pk = pk)
    if request.method == 'POST':
        form = FormSolicitudEstado(request.POST, instance = SolicitudPK)
        if form.is_valid():
            SolicitudPK = form.save(commit=False)
            SolicitudPK = Post.objects.get(pk = pk)

            topProductoresCProductos = []
            productoscProductor = Producto.objects.all()
            print(productoscProductor)
            
            for prod in productoscProductor:
                productorunico = User.objects.get(username=prod.autor.username,disponible=True)
                try:
                    if Contrato.objects.get(usuario=productorunico,vigencia=True):
                        topProductoresCProductos.append(productorunico)
                except Contrato.DoesNotExist:
                    messages.error(request, f'No hay productores con contrato disponibles')

    
            cantidadnecesaria= SolicitudPK.cantidad_necesaria
            productonecesario = SolicitudPK.productoreq
            calibrenecesario = SolicitudPK.calibre
            variedadnecesaria = SolicitudPK.variedad
            refrigeracionnecesaria = SolicitudPK.refrigeracion
            estadoactual = form.cleaned_data['EstadoSolicitud']
            
            '''Solicitud aprobada'''
            if estadoactual == "1":
                topProductos = []
                topProductos1 = []
                topcaso3 = []
  
                for productor in topProductoresCProductos:
                    try:
                        producto1 = Producto.objects.get(autor=productor,variedad=variedadnecesaria, producto=productonecesario, calibre=calibrenecesario,Saldo=False)
                        print(str(producto1.autor)+str(producto1.producto)+str(producto1.variedad))
                        if not producto1 in topProductos:
                            topProductos.append(producto1)
                    except Producto.DoesNotExist:
                        print(str(producto1)+"califica en calibre/producto/saldo")
                print(topProductos)
                for prodidoneo in topProductos:                    
                    if prodidoneo.cantidad >= cantidadnecesaria:
                        topProductos1.append(prodidoneo)                        
                    else: 
                        topcaso3.append(prodidoneo)
                        print(prodidoneo)

                try:
                    min_precio = min(topProductos1, key=attrgetter('precio'))
                    min_precio = min_precio.precio
                except:
                    print("No hay ningun productor para calcular el precio minimo ")

                if not SolicitudPK.producto.exists():

                    if any(topProductos1):                
                        print(len(topProductos1))
                        if len(topProductos1) == 1:
                            for ganador in topProductos1:
                                if ganador.precio == min_precio:
                                    productoganador = ganador     

                                    #posiblidad de bloque pl sql, cuando el producto llege a 0,borrar la fila completa del producto
                                    productoganador.cantidad = productoganador.cantidad - cantidadnecesaria
                                    productoganador.save()
                                    #cantidad actual ya n       o seria necesaria
                                    SolicitudPK.cantidad_actual = cantidadnecesaria
                                    SolicitudPK.EstadoSolicitud = "4"
                                    SolicitudPK.producto.add(productoganador)


                                    postprod= Post_productos.objects.get(post=SolicitudPK, producto=productoganador)
                                    postprod.cantidad_pujada = cantidadnecesaria
                                    postprod.save()

                                    SolicitudPK.save()
                                    
                                    #ENVIAR CORREO AL PRODUCTOR PARA QUE LLEVE SUS PRODUCTOS A BODEGA
                                    pcorreo= productoganador.autor.email
                                    '''
                                    send_mail(
                                        'PRODUCTOR!lleva tus productos a bodega central!',
                                        'Tus productos ganaron la subasta, el siguiente paso es llevarlos a bodega central',
                                        'maipo_grande@gmail.com',
                                        [pcorreo],
                                        fail_silently=False,
                                    )
                                    '''
                                    messages.success(request, f'Se ha notificado al productor para que lleve sus productos a bodega')        
                        #Si hay mas de un productor que califica en calibre,cantidad 
                        elif len(topProductos1) >= 2:
                            print('========================topproductos1')
                            print(topProductos1)
                            #Se seleccionan los dos primeros (Top 2)
                            for ganador in topProductos1[:2]:
                                #si tienen el mismo precio(el minimo)
                                if ganador.precio == min_precio:
                                    productoganador = ganador     
                                    #Se divide la cantidad en dos
                                    cantidaddividida= cantidadnecesaria//2
                                    productoganador.cantidad = productoganador.cantidad - cantidaddividida
                                    productoganador.save()
                                    print('========================productoganador.cantidad')
                                    print(productoganador.cantidad)
                                    #se actualiza la solicitud a subasta de transporte y la cantidad actual se llena
                                    #SolicitudPK.cantidad_actual = SolicitudPK.cantidad_actual+cantidaddividida
                                    SolicitudPK.cantidad_actual = cantidadnecesaria
                                    SolicitudPK.EstadoSolicitud = "4"
                                    #productores ganadores ya no estan disponibles
                                    productoganador.autor.disponible=False
                                    #Debe ser un arreglo de productores(pueden ser mas de un productor ganador)

           
                                    postprod= Post_productos.objects.get(post=SolicitudPK, producto=productoganador)
                                    postprod.cantidad_pujada = cantidaddividida
                                    postprod.save()
                                    SolicitudPK.producto.add(productoganador)


                                    #ENVIAR CORREO AL PRODUCTOR PARA QUE LLEVE SUS PRODUCTOS A BODEGA
                                    '''
                                    pcorreo= productoganador.autor.email
                                    send_mail(
                                        'PRODUCTOR!lleva tus productos a bodega central!',
                                        'Tus productos ganaron la subasta, el siguiente paso es llevarlos a bodega central',
                                        'maipo_grande@gmail.com',
                                        [pcorreo],
                                        fail_silently=False,
                                    )
                                    '''
                                else:
                                    print(str(ganador)+' No tiene el precio minimo para participar en la subasta')
                            SolicitudPK.save()        
                            messages.success(request, f'Se ha notificado a los productores para que lleven sus productos a bodega')
                    else:
                        topcaso3.sort(key = operator.attrgetter('cantidad'),reverse=True)
                        print(topcaso3)
                        if any(topcaso3):
                            cntsumada = 0
                            prodpuja= []
                            cntprod=[]
                            for prod in topcaso3:
                                if cntsumada <= cantidadnecesaria:
                                    cntsumada=cntsumada+prod.cantidad
                                    print('cantidad prod: '+str(prod.cantidad))
                                    print('cantidad sumanda: '+str(cntsumada))
                                    prodpuja.append(prod)
                                    cntprod.append(prod.cantidad)

                            if cntsumada >= cantidadnecesaria:
                                diffultimo = cntsumada-cantidadnecesaria
                                for p in prodpuja:
                                    if p==prodpuja[-1]:
                                        SolicitudPK.producto.add(p, through_defaults={'cantidad_pujada':p.cantidad-diffultimo })
                                        
                                    else:
                                        SolicitudPK.producto.add(p, through_defaults={'cantidad_pujada':p.cantidad })
                                        
                                    SolicitudPK.cantidad_actual = cantidadnecesaria
                                    SolicitudPK.EstadoSolicitud = "4"
                                    SolicitudPK.save()

                                    p.cantidad = p.cantidad-p.cantidad                        
                                    p.save()

                                    #ENVIAR CORREO AL PRODUCTOR PARA QUE LLEVE SUS PRODUCTOS A BODEGA
                                    '''
                                    pcorreo= p.autor.email
                                    
                                    send_mail(
                                        'PRODUCTOR!lleva tus productos a bodega central!',
                                        'Tus productos ganaron la subasta, el siguiente paso es llevarlos a bodega central',
                                        'maipo_grande@gmail.com',
                                        [pcorreo],
                                        fail_silently=False,
                                    )
                                    '''
                                diffultimo = cntsumada-cantidadnecesaria
                                
                                prodpuja[-1].cantidad = prodpuja[-1].cantidad + diffultimo
                                prodpuja[-1].save() 

                                
                                messages.success(request, f'Se ha notificado al productor para que lleve sus productos a bodega')    
                                print(SolicitudPK.producto.all())   
                        else:
                            SolicitudPK.EstadoSolicitud= '3'
                            messages.error(request, f'No hay productos suficientes para satisfacer el pedido.')
                print(SolicitudPK.producto.exists())
                if SolicitudPK.producto.exists():
                    #SUBASTA DE TRANSPORTE
                    '''==TABLA DE TAMAÑOS TRANSPORTISTA==
                    TAMAÑO =(
                    ("1", "Liviano "),
                    ("2", "Mediano"),
                    ("3", "Pesado"),
                    )
                    '''
                    #Pallet: 1000 x 1000 mm
                    Cajas= 32.0
                    cantidad = SolicitudPK.cantidad_necesaria
                    pallets=-(-cantidad // Cajas)

                    tamañonecesario = ''
                    if pallets >= 1 and pallets <=12:
                        tamañonecesario= '1'
                    elif pallets >12 and pallets <=32:
                        tamañonecesario= '2'
                    elif pallets > 32:
                        tamañonecesario = '3'

                    print(tamañonecesario)


                    transportes=[]
                    #Se trae solo a los transportistas disponibles
                    transps = User.objects.filter(rol="4",disponible=True)
                    print(transps)
                    for ut in transps:
                        try:
                            tg=Transporte.objects.get(transportista=ut,tamaño=tamañonecesario, refrigeracion=refrigeracionnecesaria)
                            try:
                                if Contrato.objects.get(usuario=ut,vigencia=True):
                                    transportes.append(tg)
                            except Contrato.DoesNotExist:
                                print('Transportista '+str(ut.username)+" no tiene contrato vigente")

                        except:
                            print('Transportista '+str(ut.username)+" no califica por disponibilidad/tamaño/refrigeracion")
                    print(transportes)
                    try:
                        min_tarifa = min(transportes, key=attrgetter('tarifa'))
                    except:
                        print("No hay ningun transportista para calcular el precio minimo ")


                    if len(transportes) >= 1:
                        print(transportes)
                        tganadores=[]
                        for t in transportes:
                            if t.tarifa <= min_tarifa.tarifa:
                                tganadores.append(t)

                        tganador=tganadores[0]

                        print(tganadores)
                        if tganador.tarifa <= min_tarifa.tarifa:
                            print(str(tganador.tarifa)+str(min_tarifa.tarifa))
                            SolicitudPK.transportista = tganador.transportista
                            SolicitudPK.transporte = tganador
                            #NOTIFICAR AL TRANSPORTISTA DE HABER GANADO LA SUBASTA
                            '''
                            tcorreo = tganador.transportista.email
                            destino = productoganador.autor.direccion
                            send_mail(
                                'SUBASTA DE TRANSPORTE ',
                                'Acabas de ganar la subasta de transporte y fuiste seleccionado para transportar los productos:\nDestino: ',
                                'maipo_grande@gmail.com',
                                [tcorreo],
                                fail_silently=False,
                            )
                            '''
                            if SolicitudPK.EstadoSolicitud == "10":
                                SolicitudPK.EstadoSolicitud = "10"
                                tganador.transportista.disponible=False
                                tganador.transportista.save()
                                SolicitudPK.save()
                                messages.success(request, f'Se ha escogido un transportista adecuado para el envio.')
                            elif SolicitudPK.EstadoSolicitud == "6":
                                SolicitudPK.EstadoSolicitud = "6"
                                tganador.transportista.disponible=False
                                tganador.transportista.save()
                                SolicitudPK.save()
                                messages.success(request, f'Se ha escogido un transportista adecuado para el envio.')
                            else:
                                SolicitudPK.EstadoSolicitud = "5"
                                tganador.transportista.disponible=False
                                tganador.transportista.save()
                                SolicitudPK.save()
                                messages.success(request, f'Se ha escogido un transportista adecuado para el envio.')
                    elif len(transportes) == 0:
                        print("No hay transportistas disponibles en este momento")
                        messages.error(request, f'No hay transportistas que cumplan los requisitos en este momento, vuelve a intentarlo mas tarde.')

            '''Solicitud Pendiente'''
            if estadoactual == "3":
                SolicitudPK.EstadoSolicitud = '3' 
            '''Rechazado'''
            if estadoactual == "2":
                SolicitudPK.EstadoSolicitud = '2' 


        SolicitudPK.save()  
        return redirect('/Solicitudes')
    else:  
        form = FormSolicitudEstado(instance=SolicitudPK)   
        context ={'form':form,}
        return render(request, 'modificarsoli.html', context)
def modificarSolicitudTransportista(request,pk):
    cart = Cart(request)
    soli= Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormSolicitudEstadoTransportista(request.POST,instance=soli)
        if form.is_valid():
            soli = form.save(commit=False)
            soli = Post.objects.get(pk = pk)
            soli.EstadoSolicitud = form.cleaned_data['EstadoSolicitud']

            if soli.EstadoSolicitud == "13":
                inputdni = request.POST.get('dni')

                dni = soli.cliente.dni
                print(dni)
                print(inputdni)
                if dni == inputdni:
                    soli.transporte.disponible = True
                    soli.save()
                    messages.success(request, f'Comprobacion de destinatario correcta')
                    return redirect('/solicitudesTransportista')
                else:
                    messages.error(request, f'El dni del cliente no coincide con el de la solicitud.')
                
            elif soli.EstadoSolicitud != "13":
                soli.save() 
                messages.success(request, f'Guardado exitosamente')
                return redirect('/solicitudesTransportista')
    else:
        form = FormSolicitudEstadoTransportista(instance=soli)
    context = { 'form': form }
    return render(request, 'modificarsoli.html', context)
def modificarSolicitudRevisor(request, pk):
    cart = Cart(request)
    soli= Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormSolicitudEstadoRevisor(request.POST,instance=soli)
        if form.is_valid():
            soli = form.save(commit=False)
            soli = Post.objects.get(pk = pk)
            soli.EstadoSolicitud = form.cleaned_data['EstadoSolicitud']
            soli.save()
            if soli.transportista:

                messages.success(request, f'Revision aprobada, el transportista ya puede llevar los productos')
            else:
                messages.warning(request, f'Revision aprobada, pero aun falta asignar un transportista al pedido')

            return redirect('/solicitudesRevisor')
    else:
        form = FormSolicitudEstadoRevisor(instance=soli)
    context = { 'form': form }
    return render(request, 'modificarsoli.html', context)

def modificarSolicitudProductor(request, pk):
    cart = Cart(request)

    enbodega=[]
    soli= Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormSolicitudEstadoProductor(request.POST,instance=soli)
        if form.is_valid():
            soli = form.save(commit=False)
            soli = Post.objects.get(pk = pk)
            soli.save()
            soli.EstadoSolicitud = form.cleaned_data['EstadoSolicitud']
            if soli.EstadoSolicitud == '6':
                
                for p in soli.producto.all():
                    Post_producto =Post_productos.objects.get(post=soli, producto=p)
                    if p.autor == request.user:
                        Post_producto.enbodega=True
                        Post_producto.save()
                    enbodega.append(Post_producto.enbodega)

                cantprod = len(soli.producto.all())
                n= 0
                for e in enbodega:
                    if e == True:
                        n=n+1
                if cantprod == n:
                    soli.EstadoSolicitud = '6'
                    soli.save()
                    
                print(cantprod)
                print(n)
            messages.success(request, f'Has avisado que tus productos estan en bodega')
            return redirect('/solicitudesProductor')
    else:
        form = FormSolicitudEstadoProductor(instance=soli)
    context = { 'form': form }
    return render(request, 'modificarsoli.html', context)
def modificarSolicitudClienteExterno(request, pk):
    cart = Cart(request)
    soli= Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormSolicitudClienteExterno(request.POST,instance=soli)
        if form.is_valid():
            soli = form.save(commit=False)
            soli = Post.objects.get(pk = pk)
            soli.EstadoSolicitud = form.cleaned_data['EstadoSolicitud']
            #SI ELIJE "PAGAR" ENTONCES DESPLEGAR EL WEBPAY:
            #CALCULO TOTAL DIVIDIDO ENTRE LOS PRODUCTORES 
            if soli.EstadoSolicitud == "14":
                totalprods=0
                cantidadprods = len(soli.producto.all())
                cantidaddivida = soli.cantidad_actual//cantidadprods
                for p in soli.producto.all():
                    totalprods= totalprods+ (cantidaddivida* p.precio)                
                print(totalprods)
                #Se suma la tarifa al total y se agrega la comision (3%)
                total= (soli.transporte.tarifa + totalprods) *1.03
                total = int(total)
                soli.save()
                return redirect('/pagar/'+str(total) +'/'+str(pk))
            
            messages.warning(request, f'Pedido rechazado, se notificará al seguro para su devolución')
            return redirect('/solicitudesClienteExterno')
    else:
        form = FormSolicitudClienteExterno(instance=soli)
    context = { 'form': form }
    return render(request, 'modificarsoli.html', context)
def registrarTransporte (request):
    cart = Cart(request)
    if request.method == 'POST':
        form = FormRegistrarTransporte(request.POST)
        if form.is_valid():
            transp = form.save(commit=False)
            transp.transportista = request.user
            transp.save()
            messages.success(request, f'Transporte Registrado')
            return redirect('/registrarTransporte')
    else:
        form = FormRegistrarTransporte()
    context = { 'form': form }
    return render(request, 'registrarTransporte.html', context)

def transportesRegistrados(request):
    cart = Cart(request)
    transp = Transporte.objects.filter(transportista=request.user)
    context={'transp':transp}

    return render(request, 'transportesRegistrados.html', context)




def Ventalocal(request):
    cart = Cart(request)
    products = Producto.objects.filter(Saldo=True)
    context={'products':products}
    cart = Cart(request)
    return render(request, 'Venta-local.html', context )


'''Carrito funcional'''

@csrf_protect
def add_product_catalogo(request, product_id):
    cart = Cart(request)
    cantidadacomprar=0
    product = Producto.objects.get(pk=product_id)

    for (key, value) in request.session['cart'].items():
        print(value['product_id'])
        print(product.pk)
        if value['product_id'] == product.pk: 
            cantidadacomprar= product.cantidad- int(value['quantity'])
    if cantidadacomprar > 0:
        cart.add(product=product)
        messages.success(request, f'{product.get_producto_display()} agregado al carrito')
    else:
        messages.warning(request, f'No quedan mas unidades de este producto') 

    return redirect("/Venta-local")


def add_product_carrito(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.add(product=product)
    return redirect("/carrito.html")




@csrf_protect
def remove_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.remove(product)
    return redirect("/carrito.html")


@csrf_protect
def decrement_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.decrement(product=product)
    return redirect("/carrito.html")


@csrf_protect
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/carrito.html")

def webpay(request):
    cart = Cart(request)
    total = 0
    FprecioC = 0
    cart = Cart(request)
    buy_order = str(1)
    session_id = str(1)
    return_url = 'http://127.0.0.1:8000/terminarsaldo'
    total = 0
    FprecioC = 0
    if request.user.is_authenticated:
        for key, value in request.session['cart'].items():
            total = total + (float(value['price']) * value['quantity'])
            # FprecioC=(f'{total:.3f}')
            FprecioC= int(total)
    amount = FprecioC
    try:
        response = Transaction().create(buy_order, session_id, amount, return_url)
        print(amount)
        return render(request, 'carrito.html', {"response":response})
    except TransbankError as e:
        print(e.message)
        return render(request, 'carrito.html', {})


def webpaycommit(request):
    cart = Cart(request)
    productos= []
    cantidades=[]
    for key,value in request.session['cart'].items():
        
        cantidadpujada = int(value['quantity'])
        id = value['product_id']

        product = Producto.objects.get(pk=id) 
        product.cantidad= product.cantidad-cantidadpujada
        
        
        
        productos.append([product, cantidadpujada])


    print(productos)
    token = request.GET.get("token_ws")
    response = Transaction().commit(token)  
    response['transaction_date'] = datetime.strptime(response['transaction_date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    return render(request, 'terminarsaldo.html',{"token": token,"response": response, "productos":productos})
    

def webpayplus_reembolso(request):
    cart = Cart(request)
    token = request.POST.get("token_ws")
    amount = request.POST.get("amount")
    try:
        response = Transaction().refund(token, amount)
        print(response)
        print(token)
        return render(request, 'reembolso.html', {"token":token, "amount": amount, "response":response})
    except TransbankError as e:
        print(e.message)
    return render(request, 'reembolso.html', {})

def webpayplus_anular(request):
    cart = Cart(request)
    return render(request, 'anular.html', {})