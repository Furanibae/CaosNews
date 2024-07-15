from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .decorators import group_required
from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.renderers import JSONRenderer
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TimezoneSerializer
from django.utils.timezone import localtime
import json
import requests
from django.http import JsonResponse
from django.views import View
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt


from .models import *
from .models import Periodista, Noticia, Subscription, Cart, CartItem , Order, PurchaseHistory
from .forms import *
from .forms import LoginForm
from .forms import NoticiaForm

from .serializers import *
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser

from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile


#=======viewset API=============================================================

class TipoPeriodistaViewSet(viewsets.ModelViewSet):
    queryset = TipoPeriodista.objects.all().order_by('id')
    serializer_class=TipoPeriodistaSerializers
    renderer_classes=[JSONRenderer]

    
class PeriodistaViewSet(viewsets.ModelViewSet):
    queryset = Periodista.objects.all().order_by('id')
    serializer_class=PeriodistaSerializers
    renderer_classes=[JSONRenderer]


#===================================================================

def index(request):
    return render(request, 'core/index.html')
@login_required
def formulario(request):
    return render(request, 'core/formulario.html')
def detalle(request):
    return render(request, 'core/detalle.html')
def periodista(request):
    return render(request, 'core/periodista.html')
def vistaUser(request):
    return render(request, 'core/vistaUser.html')
def indexAdmin(request):
    return render(request, 'core/periodistas/indexAdmin.html')
def add(request):
    return render(request, 'core/periodistas/crud/add.html')
def update(request):
    return render(request, 'core/periodistas/crud/update.html')


def account_locked(request):
    return render(request, 'core/account_locked.html')


@login_required
def perfil(request):
    return render(request, 'core/perfil.html')
@login_required
def checkout(request):
    return render(request, 'core/checkout.html')

def login(request):
    return render(request, 'core/registration/login.html')

def register(request):
    aux ={
        'form':Customusercreation()
    }
    return render(request, 'core/registration/register.html',aux)


#=====================CRUD PERIODISTA=========================

def periodistas(request):
    periodistas = Periodista.objects.all()
    aux = {
        'lista': periodistas
    }
    return render(request, 'core/periodistas/indexAdmin.html', aux)




def add(request):
    aux = {
        'form' : PeriodistaForm()
    }
    
    if request.method == 'POST':
        formulario = PeriodistaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            aux['msj'] = 'Periodista agregado correctamente!'
        else:
            aux['form'] = formulario
            aux['msj'] = 'Error, no se pudo almacenar el empleado!'
    return render(request, 'core/periodistas/crud/add.html', aux)       


def update(request, id):
    periodista = Periodista.objects.get(id=id)
    aux = {
        'form' : PeriodistaForm(instance=periodista)
    }
    if request.method == 'POST':
        formulario = PeriodistaForm(data=request.POST, instance = periodista)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            aux['msj'] = 'Periodista modificado correctamente!'
        else:
            aux['form'] = formulario
            aux['msj'] = 'Error, no se pudo modificar!'
           
    return render(request, 'core/periodistas/crud/update.html', aux)



def periodistasdelete(request, id):
    periodista = Periodista.objects.get(id=id)
    periodista.delete()
    return redirect(to="indexAdmin")

#=====================FIN CRUD PERIODISTA=========================

def login_view(request):
    form = AuthenticationForm()
    return render(request, 'core/registration/login.html', {'form': form})

def register(request):
    msj = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            msj = 'Registro exitoso!'
           
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/registration/register.html', {'form': form, 'msj': msj})



#====================NOTICIA===========================

@group_required('Editor')
def confirmar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    noticia.estado = 'aceptada'
    noticia.save()
    return redirect('listanoticias')

def noticias_aceptadas(request):
    noticias_list = Noticia.objects.filter(estado='aceptada').order_by('-fecha')
    
    paginator = Paginator(noticias_list, 3) 
    page = request.GET.get('page')
    
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        noticias = paginator.page(1) 
    except EmptyPage:
        noticias = paginator.page(paginator.num_pages)
    
    return render(request, 'core/noticias_aceptadas.html', {'noticias': noticias})


@group_required('Periodistas')
@permission_required('core.add_noticia')
def procesar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.usuario = request.user
            form.save()
            return redirect('noticias_usuarios')
    else:
        form = NoticiaForm()
    
    return render(request, 'formulario.html', {'form': form})

@group_required('Periodistas')
@permission_required('core.view_noticia')
def noticias_usuarios(request):
    noticias = Noticia.objects.filter(usuario=request.user)
    return render(request, 'noticiasUsuarios.html', {'noticias': noticias})


@group_required('Periodistas')
@permission_required('core.delete_noticia')
def borrar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    if request.method == 'POST':
        noticia.delete()
        return redirect('noticias_usuarios')
    return redirect('noticias_usuarios')

@group_required('Periodistas')
@permission_required('core.change_noticia')
def editar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id) 
    
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('noticias_usuarios')
    else:
        form = NoticiaForm(instance=noticia)
    
    return render(request, 'core/formulario.html', {'form': form, 'noticia': noticia})

@group_required('Editor')
@permission_required('core.view_noticia')
def listanoticias(request):
    noticias = Noticia.objects.all()
    return render(request, 'listanoticias.html', {'noticias': noticias})

@group_required('Editor')
@permission_required('core.change_noticia')
def cambiar_estado_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        noticia.estado = nuevo_estado
        noticia.save()
        return redirect('listanoticias')
    
    return redirect('listanoticias')


#===========================API HORA=================================
class TimezoneView(APIView):
    def get(self, request, format=None):
        current_time = localtime(timezone.now())
        current_timezone = str(timezone.get_current_timezone())
        return Response({'timezone': current_timezone, 'current_time': current_time})
    

#==================================API mindicador===============================
class ExchangeRateView(View):
    def get(self, request, *args, **kwargs):
        response = requests.get('https://mindicador.cl/api/dolar')
        if response.status_code == 200:
            data = response.json()
            exchange_rate = data['serie'][0]['valor']
            return JsonResponse({'exchange_rate': exchange_rate})
        else:
            return JsonResponse({'error': 'Could not retrieve exchange rate'}, status=500)
        

#==============================CRUD CARRITO===========================================

@login_required
def add_to_cart(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, subscription=subscription)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    subtotal = sum(item.subscription.price * item.quantity for item in cart_items)
    descuentos = 0 
    total = subtotal - descuentos
    total_amount = '{:.2f}'.format(total)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'descuentos': descuentos,
        'total': total,
        'total_amount': total_amount,
        'cart_count': cart_items.count(),
    }
    
    return render(request, 'core/cart.html', context)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    
    if cart_item.cart.user != request.user:
        return redirect('cart_view')
    
    cart_item.delete()
    return redirect('cart_view')

@login_required

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            cart_item.quantity += 1
        elif action == 'remove':
            cart_item.quantity -= 1

            if cart_item.quantity <= 0:
                cart_item.delete() 
                
                return redirect('cart_view')

        cart_item.save()

    return redirect('cart_view')

#=========== Boleta PDF ================

@login_required
@csrf_exempt
def complete_purchase(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            return JsonResponse({'status': 'fail', 'message': 'No items in cart'}, status=400)
        
        subtotal = sum(item.subscription.price * item.quantity for item in cart_items)
        descuentos = 0  # Asegúrate de manejar los descuentos según tus reglas de negocio
        total = subtotal - descuentos

        with transaction.atomic():
            new_order = Order.objects.create(user=request.user, total=total)
            for item in cart_items:
                PurchaseHistory.objects.create(
                    user=request.user,
                    order=new_order,
                    subscription=item.subscription,
                    quantity=item.quantity,
                    total_amount=item.subscription.price * item.quantity
                )
            cart_items.delete()  # Vaciar el carrito después de la compra

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'fail'}, status=400)



@login_required
def ver_boleta(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cart_items = CartItem.objects.filter(cart__user=request.user)
    subtotal = sum(item.subscription.price * item.quantity for item in cart_items)
    descuentos = 0  # Asegúrate de calcular los descuentos si aplican
    total = subtotal - descuentos
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'descuentos': descuentos,
        'total': total,
    }
    
    return render(request, 'core/invoice.html', context)

@login_required
def historial_de_compras(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/historialdecompra.html', {'orders': orders})

@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    purchase_items = PurchaseHistory.objects.filter(order=order)

    subtotal = sum(item.subscription.price * item.quantity for item in purchase_items)
    descuentos = 0
    total = subtotal - descuentos

    context = {
        'purchase_items': purchase_items,
        'subtotal': subtotal,
        'descuentos': descuentos,
        'total': total,
        'order': order
    }

    html_string = render_to_string('core/invoice.html', context)
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    return response