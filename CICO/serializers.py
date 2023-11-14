from rest_framework import serializers
from .models import Cats

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cats
        fields = '__all__'