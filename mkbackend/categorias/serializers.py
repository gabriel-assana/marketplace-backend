from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from categorias.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Categoria
        fields = '__all__'

class EditarCategoriaSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Categoria
        fields = ['id', 'nome']