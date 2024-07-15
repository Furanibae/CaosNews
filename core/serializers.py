from rest_framework import serializers
from .models import *
from django.utils import timezone



class TipoPeriodistaSerializers(serializers.ModelSerializer):
    class Meta:
        model = TipoPeriodista
        fields = '__all__'


class PeriodistaSerializers(serializers.ModelSerializer):
    tipo = TipoPeriodistaSerializers(read_only=True)
    class Meta:
        model = Periodista
        fields = '__all__'

class TimezoneSerializer(serializers.Serializer):
    timezone = serializers.CharField(default=str(timezone.get_current_timezone()))

class SubscriptionSerializer(serializers.ModelSerializer):
    amount_in_clp = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'price', 'description', 'amount_in_clp']

    def get_amount_in_clp(self, obj):
        request = self.context.get('request')
        
        # Obtener el tipo de cambio desde el contexto de la solicitud (si se pasa como contexto)
        usd_to_clp = request.usd_to_clp if hasattr(request, 'usd_to_clp') else 800
        
        # Calcular el monto en CLP
        amount_in_usd = obj.price  # Suponiendo que price es en USD
        amount_in_clp = amount_in_usd * usd_to_clp

        return amount_in_clp    