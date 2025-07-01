from rest_framework import serializers
from .models import *

class vehical_serializer(serializers.ModelSerializer):
    class Meta:
        model = Vehical
        fields = ['veh_id','veh_number','veh_default_mobile']
