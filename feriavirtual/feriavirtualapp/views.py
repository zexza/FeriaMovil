from ast import Try
from datetime import datetime
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
from operator import attrgetter
from django.core.mail import send_mail
from .cart import Cart
from .context_processor import cart_total_amount
from django.views.decorators.csrf import csrf_protect
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pyodbc
import json
import numpy as np


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
                messages.error(request, f'Este productor ya tiene un contrato vigente.')
            else:  
                cont.fecha_inicio = form.cleaned_data['fecha_inicio']
                cont.fecha_termino = form.cleaned_data['fecha_termino']
                if cont.fecha_inicio > cont.fecha_termino:
                    messages.error(request, f'La fecha de inicio no puede ser mayor a la de termino del contrato')
                else:
                    cont.vigencia = True
                    form.save()
                    messages.success(request, f'Contrato para productor {cont.username} creado')
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
    elif request.user.rol =="1" or request.user.rol =="5":
        solis = Post.objects.filter(pk=pk)
    else:
        solis = Post.objects.filter(usuario=request.user,pk=pk)
    context = {'solis':solis}
    return render(request, 'seguimiento.html',context)

def seguimientoLista(request):
    user= request.user
    cart = Cart(request)
    if request.user.is_staff:
        solis = Post.objects.all()
    elif request.user.rol =="5":
         solis = Post.objects.all()
    elif request.user.rol =="1":
        post = Post.objects.all()
        for p in post:
            for prod in p.producto.filter(autor=user):
                solis = Post.objects.filter(producto=prod)
    elif request.user.rol =="2" or request.user.rol =="3":
        solis = Post.objects.filter(cliente=user)
    else:
        solis = Post.objects.filter(usuario=request.user)
    context = {'solis':solis}
    return render(request, 'seguimientoLista.html',context)


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

DATABASES = {
'default': {
'ENGINE': "sql_server.pyodbc",
'HOST': "186.78.38.134\DESKTOP-A7GEGG2\SQL2019TAB,14334",
'USER': "sa",
'PASSWORD': "Pvsa**2021",
'NAME': "sqlite6",
'OPTIONS': {"driver": "ODBC Driver 17 for SQL Server", 
'host_is_server': True
},
}
}


def connection(request):
    s = '186.78.38.134\DESKTOP-A7GEGG2\SQL2019TAB,14334' #Your server name 
    d = 'sqlite6' #name bd  
    u = 'sa' #Your login
    p = 'Pvsa**2021' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn 
    

def Consulta(request):
    if request.method == 'POST':
        form = FormEstadoSolicitud(request.POST)
        if form.is_valid():
            print(form)
        return render(request, 'Consulta.html',)
            
    else:
        form = FormEstadoSolicitud()
    

    

    #Fecha_json = json.dumps([P.fecha_creacion for P in PostObj], cls=DTEncoder)
    #Usuario_json = json.dumps([P.usuario for P in PostObj])
    select=('SELECT        dbo.feriavirtualapp_post.id, dbo.feriavirtualapp_producto.precio, dbo.feriavirtualapp_producto.autor_id, dbo.feriavirtualapp_post_producto.post_id, dbo.feriavirtualapp_post.EstadoSolicitud,  dbo.feriavirtualapp_post.cantidad_necesaria, dbo.feriavirtualapp_post.transporte_id, dbo.feriavirtualapp_post.fecha_creacion FROM            dbo.feriavirtualapp_post INNER JOIN dbo.feriavirtualapp_post_producto ON dbo.feriavirtualapp_post.id = dbo.feriavirtualapp_post_producto.post_id INNER JOIN dbo.feriavirtualapp_producto ON dbo.feriavirtualapp_post_producto.producto_id = dbo.feriavirtualapp_producto.id')    
    conn = connection(request)
    df_merge_dataframe = pd.read_sql(select, conn)
    post = Post.objects.all()
    productos= Producto.objects.all()
    
    
    
    #Fecha_json = json.dumps([P.fecha_creacion for P in PostObj], cls=DTEncoder)
    #Usuario_json = json.dumps([P.usuario for P in PostObj])
    
    df_user_cliente = pd.DataFrame.from_records(list(User.objects.all().values('id','username')),)
    df_trasporte = pd.DataFrame.from_records(list(Transporte.objects.all().values('id','tarifa')),)
    

        
    DfPostPk= pd.DataFrame([str(p.pk) for p in post], columns=['pk'])
    DfUsuario = pd.DataFrame([str(p.cliente) for p in post], columns=['Usuario'])
    DfTransportista = pd.DataFrame([str(p.transportista) for p in post], columns=['Transportista'])
    DfFecha = pd.DataFrame([p.fecha_creacion for p in post], columns=['Fecha'])
    DfProducto = pd.DataFrame([str(p.producto) for p in post], columns=['Producto'])
    DfProductoVariedad= pd.DataFrame([str(p.variedad) for p in post], columns=['variedad'])
    
    DataframeConsulta =  pd.concat([DfUsuario, DfFecha,DfTransportista,DfProducto,DfProductoVariedad],axis=1)
    DataframeConsulta = DataframeConsulta.fillna(0)
    
    
    
    DfproductosPrecio = pd.DataFrame([str(p.precio) for p in productos], columns=['precio'])
    DfProductosProducto = pd.DataFrame([str(p.producto) for p in productos], columns=['producto'])
    DfProductosVariedad= pd.DataFrame([str(p.variedad) for p in productos], columns=['variedad'])
    DfProductosUsername= pd.DataFrame([str(p.autor.username) for p in productos], columns=['username'])
    
    DataframeProductos =  pd.concat([DfproductosPrecio,DfProductosProducto,DfProductosVariedad,DfProductosUsername],axis=1)

    





    #join User 
    df_merge_dataframe = pd.merge(df_user_cliente, df_merge_dataframe, left_on='id', right_on='autor_id')
    df_merge_dataframe.rename(columns = {'username':'NombreProductor',},  inplace = True)  
    df_merge_dataframe.drop('id_x', inplace=True, axis=1)
    df_merge_dataframe.drop('id_y', inplace=True, axis=1)
    df_merge_dataframe=df_merge_dataframe.sort_values(by=['post_id'])

    
    dfGroupbyPostIdCount = df_merge_dataframe.groupby(['post_id'])['post_id'].count()
    dfGroupbyPostIdCount= pd.DataFrame(dfGroupbyPostIdCount)
    dfGroupbyPostIdCount.rename(columns = {'post_id':'Cantidaddeproductores', }, inplace = True) 
    
    df_merge_dataframe = pd.merge(df_merge_dataframe, dfGroupbyPostIdCount, left_on='post_id', right_on='post_id')
    
    PrecioFinalProductor=df_merge_dataframe['precio'] * df_merge_dataframe['cantidad_necesaria']/df_merge_dataframe['Cantidaddeproductores']
    df_merge_dataframe.insert(2, "PrecioFinalProductor", PrecioFinalProductor, True)
    
    
    df_total_neto_productores =df_merge_dataframe['PrecioFinalProductor'].sum()
    
    df_total_neto_post = df_merge_dataframe.groupby(['post_id'])['PrecioFinalProductor'].sum()
    dfGroupbyPostIdCount= pd.DataFrame(df_total_neto_post)


    
    #Join trasporte
 
    df_merge_dataframe_trasporte = pd.merge(df_merge_dataframe, df_trasporte, left_on='transporte_id', right_on='id')
    df_merge_dataframe_trasporte=df_merge_dataframe_trasporte.sort_values(by=['post_id'])

    DfGroupbyPostTotalProductor= df_merge_dataframe_trasporte.groupby(['post_id'])['PrecioFinalProductor'].sum()
    DfGroupbyPostTotalProductor= pd.DataFrame(DfGroupbyPostTotalProductor)
    DfGroupbyPostTotalProductor.rename(columns = {'PrecioFinalProductor':'PrecioFinalPostProductor', }, inplace = True) 
    df_merge_dataframe_trasporte = pd.merge(df_merge_dataframe_trasporte, DfGroupbyPostTotalProductor, left_on='post_id', right_on='post_id')

 
    dataframeTarifaProductor=df_merge_dataframe_trasporte['PrecioFinalPostProductor']+df_merge_dataframe_trasporte['tarifa']
    df_merge_dataframe_trasporte.insert(13, "PrecioFinaltarifaproductor", dataframeTarifaProductor, True)
    
    df_merge_dataframe_trasporte.insert(14, "PrecioFinaltarifaproductorGanancia",((df_merge_dataframe_trasporte['PrecioFinaltarifaproductor']*0.3)+(df_merge_dataframe_trasporte['PrecioFinaltarifaproductor'])) , True)
    
    
    df_merge_dataframe_trasporte.insert(15, "Ganancia", (dataframeTarifaProductor)*0.3, True)
    df_merge_dataframe_trasporte.insert(16, "IdPost", df_merge_dataframe_trasporte['post_id'], True)
    
  




  




    DataframePost= pd.DataFrame(    df_merge_dataframe_trasporte.groupby(['EstadoSolicitud', 'cantidad_necesaria', 
       'fecha_creacion', 'Cantidaddeproductores', 'tarifa',
       'PrecioFinalPostProductor', 'PrecioFinaltarifaproductor',
       'PrecioFinaltarifaproductorGanancia', 'Ganancia','IdPost'])['post_id'].size())
    


    DataframePost= pd.DataFrame(  DataframePost.reset_index() )
       
    DataframePost=DataframePost.sort_values(by=['IdPost'])
    print(DataframePost)
    Df_grouPostIDPrecioFinalTotal = DataframePost['PrecioFinaltarifaproductorGanancia'].sum()
    Df_grouPostIDPrecioFinalTotal= str('{:,.0f}'.format(Df_grouPostIDPrecioFinalTotal).replace(",", "@").replace(".", ",").replace("@", "."))
    


    
    Df_grouPostIDGananciaTotal = DataframePost['Ganancia'].sum()
    Df_grouPostIDGananciaTotal= str('{:,.0f}'.format(Df_grouPostIDGananciaTotal).replace(",", "@").replace(".", ",").replace("@", "."))
    
    
    DataframeConsultaSumaProductor = DataframePost['PrecioFinalPostProductor'].sum()
    DataframeConsultaSumaProductor= str('{:,.0f}'.format(DataframeConsultaSumaProductor).replace(",", "@").replace(".", ",").replace("@", "."))
    
    
    DataframeConsultaSumaProductortarifa = DataframePost['PrecioFinaltarifaproductor'].sum()
    DataframeConsultaSumaProductortarifa= str('{:,.0f}'.format(DataframeConsultaSumaProductortarifa).replace(",", "@").replace(".", ",").replace("@", "."))

    
    

    


    GrupbyProducto = DataframeConsulta.groupby(['variedad'])['variedad'].count()

    


    

    


    
    
    
    
    
    figGeneral = go.Figure(go.Scatter(
    x=DataframePost['IdPost'],y=DataframePost['PrecioFinaltarifaproductorGanancia']))

    figGeneral.update_layout(
        xaxis_title="Solicitud ID",
        yaxis_title="Cobro Finla X Solicitud",
        title={
            'text': "Plot Title",
            'y':0.9,
            'x':0.5,
            
            'xanchor': 'center',
            'yanchor': 'top'}
        
        )
    

    chartGeneral = figGeneral.to_html()

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
    return render(request, 'Consulta.html',context)




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
            post = form.save(commit=False)
            post.cliente = form.cleaned_data['cliente']
            post.user = request.user
            post.fecha_creacion = timezone.now()
            post.imagen = request.FILES['imagen'] if 'filepath' in request.FILES else False
            post.save()
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
        #================COMPROBANTES DE PAGO==================
        #================PRODUCTORES==========================
        cantidadprods = len(soli.producto.all())
        cantidaddivida = soli.cantidad_actual//cantidadprods
        for p in soli.producto.all():
            comProd = Comprobante(usuario=p.autor,solicitud = soli,monto=p.precio * cantidaddivida)
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
            post = form.save(commit=False)
            post.usuario = request.user
            post.fecha_creacion = timezone.now()
            post.imagen = request.FILES['imagen'] if 'filepath' in request.FILES else False
            post.save()
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
            post.cliente = request.user
            post.usuario = request.user
            post.fecha_creacion = timezone.now()
            post.imagen = request.FILES['imagen'] if 'filepath' in request.FILES else False
            post.save()
            messages.success(request, f'Solicitud enviada')
            return redirect('/Solicitudes')
    else:
        form = FormVentaCliente()
    context = { 'form': form }
    return render(request, 'solicitudClientes.html',context)

def solicitudes(request):
    soli = Post.objects.filter(EstadoSolicitud__in=("3","4"))
    cart = Cart(request)
    context ={'soli':soli}
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
    post = Post.objects.all()
    for p in post:
        for prod in p.producto.filter(autor=request.user):
            solip = Post.objects.filter(producto=prod,EstadoSolicitud__in=("1","4","5"))


    context ={'solip':solip}
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
            productoscProductor = Producto.objects.filter().values_list('autor_id').distinct()
            for prod in productoscProductor:
                productorunico = User.objects.get(id=int(prod[0]),disponible=True)
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
                for productor in topProductoresCProductos:
                    try:
                        producto1 = Producto.objects.get(autor=productor,variedad=variedadnecesaria, producto=productonecesario, calibre=calibrenecesario,Saldo=False)
                        topProductos.append(producto1)
                    except Producto.DoesNotExist:
                        print("Ningun producto califica en calibre/producto/saldo")
                for prodidoneo in topProductos:                    
                    if prodidoneo.cantidad >= cantidadnecesaria:
                        topProductos1.append(prodidoneo)                        
                    else:
                        #Caso 3Cuando un productor cumple los requisitos pero no tiene la cantidad necesaria, pero hay más productores que cumplen los requisitos y pueden completar la cantidad necesaria con un precio un poco más elevado
                        print("Este productor no tiene la cantidad necesaria.")
                try:
                    min_precio = min(topProductos1, key=attrgetter('precio'))
                    min_precio = min_precio.precio
                except:
                    print("No hay ningun productor para calcular el precio minimo ")
                
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
                                print(productoganador.cantidad)
                                #se actualiza la solicitud a subasta de transporte y la cantidad actual se llena
                                #SolicitudPK.cantidad_actual = SolicitudPK.cantidad_actual+cantidaddividida
                                SolicitudPK.cantidad_actual = cantidadnecesaria
                                SolicitudPK.EstadoSolicitud = "4"
                                #productores ganadores ya no estan disponibles
                                productoganador.autor.disponible=False
                                #Debe ser un arreglo de productores(pueden ser mas de un productor ganador)
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

                    #SUBASTA DE TRANSPORTE
                    '''==TABLA DE TAMAÑOS TRANSPORTISTA==
                    TAMAÑO =(
                    ("1", "Liviano "),
                    ("2", "Mediano"),
                    ("3", "Pesado"),
                    )
                    '''
                    #Pallet: 1000 x 1000 mm
                    Cajas= 32
                    pallets=SolicitudPK.cantidad_necesaria//Cajas
                    
                    if pallets >= 192 and pallets <=384:
                        tamañonecesario= '1'
                    elif pallets >=385 and pallets <=768:
                        tamañonecesario= '2'
                    elif pallets > 768:
                        tamañonecesario = '3'

                    transportes=[]
                    #Se trae solo a los transportistas disponibles
                    transps = User.objects.filter(rol="4",disponible=True)
                    for ut in transps:
                        try:
                            tg=Transporte.objects.get(transportista=ut,tamaño=tamañonecesario, refrigeracion=refrigeracionnecesaria)
                            transportes.append(tg)
                        except:
                            print('Transportista '+str(ut.username)+" no califica por disponibilidad/tamaño/refrigeracion")
                    try:
                        min_tarifa = min(transportes, key=attrgetter('tarifa'))
                    except:
                        print("No hay ningun transportista para calcular el precio minimo ")
                    if len(transportes) == 1:
                        tganador = transportes[0]
                        print(tganador)
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
                        SolicitudPK.EstadoSolicitud = "5"
                        tganador.transportista.disponible=False
                        tganador.transportista.save()
                        SolicitudPK.save()
                        messages.success(request, f'Se ha escogido un transportista adecuado para el envio.')
                    elif len(transportes) >= 2:
                        
                        print("Hay dos transportistas")
                    elif len(transportes) == 0:
                        print("No hay transportistas disponibles en este momento")
                        messages.error(request, f'No hay transportistas que cumplan los requisitos en este momento, vuelve a intentarlo mas tarde.')

                else:
                    SolicitudPK.EstadoSolicitud = '3' 
                    messages.error(request, f'No hay productores que puedan participar en la subasta en este momento, vuelve a intentarlo mas tarde.')


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
            messages.success(request, f'Guardado exitosamente')
            return redirect('/solicitudesTransportista')
    else:
        form = FormSolicitudEstadoRevisor(instance=soli)
    context = { 'form': form }
    return render(request, 'modificarsoli.html', context)

def modificarSolicitudProductor(request, pk):
    cart = Cart(request)
    soli= Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormSolicitudEstadoProductor(request.POST,instance=soli)
        if form.is_valid():
            soli = form.save(commit=False)
            soli = Post.objects.get(pk = pk)
            soli.EstadoSolicitud = form.cleaned_data['EstadoSolicitud']
            soli.save()
            messages.success(request, f'Guardado exitosamente')
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
    product = Producto.objects.get(id=product_id)
    cart.add(product=product)
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
    if request.user.is_authenticated:
        for key, value in request.session['cart'].items():
            quantity = ( value['quantity'])
            quantity= int(quantity)
            quantity = ( value['quantity'])
            id = ( value['product_id'])
    id=id        
    quantity = quantity
    product = Producto.objects.get(id=id)    
    cantidadactual=product.cantidad     
    product.cantidad = cantidadactual - quantity
    product.save()
    #arreglar
    cart = Cart(request)
    token = request.GET.get("token_ws")
    response = Transaction().commit(token)     
    return render(request, 'terminarsaldo.html',{"token": token,"response": response})
    

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