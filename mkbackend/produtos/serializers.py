from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from produtos.models import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class CadastrarProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = ["titulo","descricao","preco","url_imagem","usuario", "categoria"]