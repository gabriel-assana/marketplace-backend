from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class CadastroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["nome", "cpf", "email", "senha"]