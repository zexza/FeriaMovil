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
    elif request.user.rol =="1":
        solis = Post.objects.filter(pk=pk)
    else:
        solis = Post.objects.filter(usuario=request.user,pk=pk)
    context = {'solis':solis}
    return render(request, 'seguimiento.html',context)

def seguimientoLista(request):
    cart = Cart(request)    
    if request.user.is_staff:
        solis = Post.objects.all()
    elif request.user.rol =="1":
        solis = Post.objects.filter(productor=request.user)
    else:
        solis = Post.objects.filter(usuario=request.user)
    context = {'solis':solis}
    return render(request, 'seguimientoLista.html',context)


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
        post = Post.objects.get(pk=pk)
        post.EstadoSolicitud = "17"
        post.save()
        messages.success(request, f'Pago exitoso.')
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
            return redirect('/')
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
            return redirect('/')
    else:
        form = FormVentaCliente()
    context = { 'form': form }
    return render(request, 'solicitudClientes.html',context)

def solicitudes(request):
    soli = Post.objects.filter(EstadoSolicitud__in=("3"))
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
    solip = Post.objects.filter(productor=request.user,EstadoSolicitud__in=("1","4","5"))

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
                productorunico = User.objects.get(id=int(prod[0]))
                try:
                    if Contrato.objects.get(usuario=productorunico,vigencia=True):
                        topProductoresCProductos.append(productorunico)
                except Contrato.DoesNotExist:
                    messages.error(request, f'No hay productores con contrato disponibles')

            cantidadnecesaria= SolicitudPK.cantidad_necesaria
            productonecesario = SolicitudPK.producto
            calibrenecesario = SolicitudPK.calibre
            refrigeracionnecesaria = SolicitudPK.refrigeracion
            estadoactual = form.cleaned_data['EstadoSolicitud']

            '''Solicitud aprobada'''
            if estadoactual == "1":
                topProductos = []
                topProductos1 = []
                for productor in topProductoresCProductos:
                    try:
                        producto1 = Producto.objects.get(autor=productor , producto=productonecesario, calibre=calibrenecesario,Saldo=False)
                        
                        topProductos.append(producto1)
                    except Producto.DoesNotExist:
                        print("Ningun producto califica en calibre/producto/saldo")
                
                for prodidoneo in topProductos:
                    
                    if prodidoneo.cantidad >= cantidadnecesaria:
                        topProductos1.append(prodidoneo)
                        
                    else:
                        print("Ningun productor tiene la cantidad necesaria.")
                try:
                    min_precio = min(topProductos1, key=attrgetter('precio'))
                    min_precio = min_precio.precio
                except:
                    print("No hay ningun productor para calcular el precio minimo ")
                
                print(len(topProductos1))
                if len(topProductos1) == 1:
                    for ganador in topProductos1:
                        if ganador.precio == min_precio:
                            productoganador = ganador     
                            productorganador = User.objects.get(username=productoganador.autor.username)
                            #posiblidad de bloque pl sql, cuando el producto llege a 0,borrar la fila completa del producto
                            productoganador.cantidad = productoganador.cantidad - cantidadnecesaria
                            productoganador.save()
                            #cantidad actual ya n       o seria necesaria
                            SolicitudPK.cantidad_actual = cantidadnecesaria
                            SolicitudPK.EstadoSolicitud = "4"
                            SolicitudPK.productor = productorganador
                            #ENVIAR CORREO AL PRODUCTOR PARA QUE LLEVE SUS PRODUCTOS A BODEGA
                            pcorreo= productorganador.email
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
                            #SUBASTA DE TRANSPORTE
                            '''==TABLA DE TAMAÑOS TRANSPORTISTA==
                            TAMAÑO =(
                            ("1", "Ligero "),
                            ("2", "Liviano"),
                            ("3", "Semi Liviano"),
                            ("4", "Mediano"),
                            ("5", "Semi esado"),
                            ("6", "Pesado"),
                            ("7", "Extra Pesado"),
                            ("8", "Mega Pesado"),
                            ("9", "Ultra Pesado"),
                            ("10", "Extra Pesado"),
                            ("11", "Giga Pesado"),
                            ("12", "Super Pesado"),
                            )
                            '''
                            #Pallet: 1000 x 1200 mm
                            #Cajas: 16 cajas
                            tamañonecesario= "1"
                            transportes = Transporte.objects.filter(tamaño=tamañonecesario, refrigeracion=refrigeracionnecesaria, disponible=True)
                            min_tarifa = min(transportes, key=attrgetter('tarifa'))

                            if len(transportes) == 1:
                                tganador = transportes.get()
                                SolicitudPK.transportista = tganador.transportista
                                SolicitudPK.transporte = tganador
                                #NOTIFICAR AL TRANSPORTISTA DE HABER GANADO LA SUBASTA
                                tcorreo = tganador.transportista.email
                                destino = productorganador.direccion
                                '''
                                send_mail(
                                    'SUBASTA DE TRANSPORTE ',
                                    'Acabas de ganar la subasta de transporte y fuiste seleccionado para transportar los productos:\nDestino: ',
                                    'maipo_grande@gmail.com',
                                    [tcorreo],
                                    fail_silently=False,
                                )
                                '''
                                SolicitudPK.EstadoSolicitud = "5"
                                tganador.disponible=False   
                                
                                messages.success(request, f'Se ha escogido un transportista adecuado para el envio.')
                            elif len(transportes) >= 2:
                                tganadores = []
                                for tganador in transportes:
                                    tganadores.append(tganador)
                                

                            elif len(transportes) == 0:
                                print("No hay transportistas que cumplan los requisitos en estos momentos")
                                messages.error(request, f'No hay transportistas que cumplan los requisitos en estos momentos')

                elif len(topProductos1) >= 2:
                    messages.error(request, f'Hay dos productores')

                elif len(topProductos1) == 0:   
                    SolicitudPK.EstadoSolicitud = '3'
                    messages.error(request, f'En este momento no hay productores que puedan satisfacer el pedido')

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

            total= soli.transporte.tarifa + 30000 * soli.cantidad_actual 
            if soli.EstadoSolicitud == "14":
                return redirect('/pagar/'+str(total) +'/'+str(pk))

                
            soli.save()
            messages.success(request, f'Guardado exitosamente')
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
    return_url = 'http://192.168.1.15:81/terminarsaldo'
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
    try:
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

    except TransbankError as e:
        messages.error(request, f'Error en la transaccion de pago.')
        error =e.message
        print(e.message)
        print(token)
        return render(request, 'terminar.html', {"error":error})   
    

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


'''Carrito funcional'''