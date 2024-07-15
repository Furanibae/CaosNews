from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import *
from rest_framework import routers
from .views import *
from . import views

from .views import add_to_cart, Cart
from .views import generate_invoice
from .views import ExchangeRateView

router= routers.DefaultRouter()
router.register('periodistas',PeriodistaViewSet)
router.register('tipoPeriodista',TipoPeriodistaViewSet)


urlpatterns = [
    path('', index, name="index"),
    path('detalle/', detalle, name="detalle"),
    path('formulario/', formulario, name="formulario"),
    path('periodista/', periodista, name="periodista"),
    path('vistaUser/', vistaUser, name="vistaUser"),
    path('periodistas/', views.periodistas, name="indexAdmin"),
    path('periodistas/crud/add/',add, name="add"),
    path('periodistas/crud/update/<id>', update, name="update"),
    path('periodistas/crud/delete/<id>', periodistasdelete, name="periodistasdelete"),
    path('registration/login/', login, name='login'),
    path('registration/register/',register, name="register"),
    path('checkout/',checkout, name="checkout"),
    #noticia


    path('procesar_noticia/', views.procesar_noticia, name='procesar_noticia'),
    path('noticias_usuarios/', views.noticias_usuarios, name='noticias_usuarios'),
    path('borrar-noticia/<int:noticia_id>/', views.borrar_noticia, name='borrar_noticia'),
    path('editar_noticia/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),
    path('listanoticias/', views.listanoticias, name='listanoticias'),
    path('cambiar_estado/<int:noticia_id>/', views.cambiar_estado_noticia, name='cambiar_estado_noticia'),
    path('confirmar_noticia/<int:noticia_id>/', views.confirmar_noticia, name='confirmar_noticia'),
    path('noticias_aceptadas/', views.noticias_aceptadas, name='noticias_aceptadas'),

    #account locked
    path('account_locked/',account_locked, name="account_locked"),
     #API
    path('api/',include(router.urls)),
    path('api/timezone/', TimezoneView.as_view(), name='timezone_api'),
    # API miindicador
    path('api/exchange-rate/', ExchangeRateView.as_view(), name='exchange_rate_api'),


    #RECUPERAR CONTRASEÑA
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    #CARRITO
    path('add_to_cart/<int:subscription_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:item_id>/', update_cart_item, name='update_cart_item'),

    #BOLETA
    

    #HISTORIAL DE COMPRAS X USER
    path('historialdecompra/',historial_de_compras, name='historial_de_compras'),

    #VER BOLETA
    path('ver-boleta/<int:order_id>/',ver_boleta, name='ver_boleta'),
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='ver_boleta'),
    path('complete_purchase/', complete_purchase, name='complete_purchase'),

    #API MINDICADOR
    path('exchange_rate/', views.ExchangeRateView.as_view(), name='exchange_rate'),
    path('api/exchange-rate/', ExchangeRateView.as_view(), name='exchange_rate_api'),   
   
]




