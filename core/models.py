from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.utils import timezone
from datetime import datetime
import requests


class TipoPeriodista(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Periodista(models.Model):

    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    TIPO_CHOICES = [
        ('periodista', 'Periodista'),
    ]  

    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    #EDAD: siempre dejar un valor o dejar los paréntesis vacíos
    #JAMAS sin paréntesis
    edad = models.IntegerField()
    direccion = models.CharField(max_length=60)
    telefono = models.CharField(max_length=12)
    habilitado = models.BooleanField(default=True)

    genero = models.CharField(max_length=10, choices=[('masculino', 'Masculino'),('femenino','Femenino')], default='masculino')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    tipo = models.ForeignKey(TipoPeriodista, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.rut




class Noticia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titular = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    nombre_redactor = models.CharField(max_length=50)
    fecha = models.DateField()
    archivo_adjunto = models.FileField(upload_to='noticias_archivos/', default='media/noticias_archivos/limon.jpg')
    categoria = models.CharField(max_length=50)
    codigo = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, default='pendiente')

    def __str__(self):
        return f"{self.usuario.username} - {self.titular}"
    

#CARRITO DE COMPRAS
class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=1)
    description = models.TextField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(Subscription, through='CartItem')

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_clp = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
       
        response = requests.get('https://mindicador.cl/api/dolar')
        if response.status_code == 200:
            data = response.json()
            exchange_rate = data['serie'][0]['valor']
            self.price_clp = int(self.subscription.price) * exchange_rate
        else:
            raise Exception('Could not retrieve exchange rate')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.subscription.name}"

 
#BOLETA

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"



#HISTORIAL DE COMPRA

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1)  # Definir un valor predeterminado
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.IntegerField(default=1)

    def __str__(self):
        return f"Purchase {self.id} by {self.user.username}"
    
#API