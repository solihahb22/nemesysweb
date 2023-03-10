from rest_framework import serializers
from .models import CoalSpec
import json

class CoalSpecWithIds(serializers.CharField):

    def to_representation(self,value):
        x = json.loads(value)
        return x

class CoalSpecSerializers(serializers.ModelSerializer):
    coalspecdata = CoalSpecWithIds()
    class Meta:
        model = CoalSpec
        fields = '__all__'
