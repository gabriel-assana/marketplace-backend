from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework import viewsets, status, filters
from usuarios.models import Usuario
from categorias.models import Categoria
from produtos.models import Produto

from usuarios.serializers import UsuarioSerializer, CadastroUsuarioSerializer
from categorias.serializers import CategoriaSerializer, EditarCategoriaSerializer
from produtos.serializers import ProdutoSerializer

from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import action, parser_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes



class CategoriaViewSet(viewsets.GenericViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        detail=False,
        methods=["get"],
        url_path="listar-categorias",
        url_name="lista-categorias"
    )
    def listar_categorias(self, request):

        if self.queryset:

            categorias = []
            for item in self.queryset:
                categorias.append({
                    "id": item.id,
                    "categoria": item.nome
                })
            return Response(
                categorias,
                status=status.HTTP_200_OK)

        return Response({
            "detail": "Não há categorias."},
            status=status.HTTP_404_NOT_FOUND
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="buscar-categoriaid",
        url_name="buscar-categoriaid"
    )
    def buscar_categoria_id(self, request, pk=None):

        categoria = get_object_or_404(Categoria, pk=pk)

        if not categoria:
            return Response({
                "detail": "Categoria não encontrada."},
                status=status.HTTP_404_NOT_FOUND    
            )
        
        serializer = {
            "id": categoria.id,
            "categoria": categoria.nome
        }
        
        return Response(
            serializer,
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='nome', 
                description='Nome da categoria para busca', 
                required=True, 
                type=OpenApiTypes.STR
            ),
        ],
        responses={200: CategoriaSerializer}
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="buscar-categoria",
        url_name="buscar-categoria"
    )
    def buscar_categoria(self, request):

        nome_categoria = request.query_params.get('nome', None)

        if nome_categoria is not None:
            categorias = Categoria.objects.filter(nome__icontains=nome_categoria)

            serializer = self.get_serializer(categorias, many=True)
            
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"detail": "O parâmetro 'nome' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST
        )

    
    @extend_schema(
        request=CategoriaSerializer,
        responses={201: CategoriaSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="cadastrar-categoria",
        url_name="cadastrar-categoria"
    )
    def cadastrar_categoria(self, request):
            
        dados = request.data

        if dados:
            serializer = self.get_serializer(data=dados)
                
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {"Sucesso": "Sucesso",
                     "detail": f'A categoria {serializer.data['nome']} foi cadastrada com sucesso.',
                     "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )

        return Response(
            {"detail": "O parâmetro 'nome' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST
        )


    @extend_schema(
        request=CategoriaSerializer,
        responses={200: CategoriaSerializer}
    )
    @action(
        detail=True,
        methods=["put"],
        url_path="editar-categaria",
        url_name="editar-categaria"
    )
    def editar_categoria(self, request, pk=None):

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors, # Retorna o motivo exato da falha na validação
            status=status.HTTP_400_BAD_REQUEST
        )


    @action(
        detail=True,
        methods=["delete"],
        url_path="excluir_categoria",
        url_name="excluir_categoria"
    )
    def excluir_categoria(self, request, pk=None):

        # categoria = get_object_or_404(Categoria, pk=pk)
        categoria = Categoria.objects.filter(pk=pk).first()

        if not categoria:
            return Response(
                {"detail": "Categoria não encontrada ou já foi excluída."},
                status=status.HTTP_404_NOT_FOUND
            )

        nome_categoria = categoria.nome

        try:
            categoria.delete()
        
            return Response({
                "detail": f'Categoria {nome_categoria} excluída com sucesso.'},
                status=status.HTTP_200_OK    
            )
        
        except Exception as e:
            return Response(
                {"detail": "Erro na exclusão da categoria",
                 "error": f"Erro na exclusão: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )




class UsuarioViewSet(viewsets.GenericViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="listar-usuarios",
        url_name="listar-usuarios"
    )
    def listar_usuarios(self, request):

        if self.queryset:

            usuarios = []
            for item in self.queryset:
                usuarios.append({
                    "id": item.id,
                    "nome": item.nome,
                    "email": item.email,
                    "super_user": item.super_user
                })
            return Response(
                usuarios,
                status=status.HTTP_200_OK
            )

        return Response({
            "detail": "Não foram encontrados os usuários."},
            status=status.HTTP_404_NOT_FOUND
        )


    @extend_schema(
        request=CadastroUsuarioSerializer,
        responses={201: CadastroUsuarioSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="cadastrar-usuario",
        url_name="cadastrar-usuario"
    )
    def cadastrar_usuario(self, request):

        dados = request.data

        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')
        cpf = dados.get('cpf')

        if all([nome, email, senha, cpf]):
            serializer = self.get_serializer(data=dados)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

        return Response(
            {"detail": "Faltam o preenchimento de campos obrigatórios"},
            status=status.HTTP_400_BAD_REQUEST
        )


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='nome', 
                description='Nome do usuário para busca', 
                required=True, 
                type=OpenApiTypes.STR
            ),
        ],
        responses={200: CategoriaSerializer}
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="buscar-usuario",
        url_name="buscar-usuario"
    )
    def buscar_usuario(self, request):

        nome_usuario = request.query_params.get('nome', None)

        if nome_usuario is not None:
            usuarios = Usuario.objects.filter(nome__icontains=nome_usuario)

            serializer = self.get_serializer(usuarios, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"detail": "O parâmetro 'nome' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST
        )


    @extend_schema(
        request=UsuarioSerializer,
        responses={200: UsuarioSerializer}
    )
    @action(
        detail=True,
        methods=["put"],
        url_path="editar-usuario",
        url_name="editar-usuario"
    )
    def editar_usuario(self, request, pk=None):

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors, # Retorna o motivo exato da falha na validação
            status=status.HTTP_400_BAD_REQUEST
        )


    @action(
        detail=True,
        methods=["delete"],
        url_path="excluir-usuario",
        url_name="excluir-usuario"
    )
    def excluir_usuario(self, request, pk=None):

        usuario = Usuario.objects.filter(pk=pk).first()

        if not usuario:
            return Response(
                {"detail": "Usuário não encontrado ou já foi excluído."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        nome_usuario = usuario.nome

        try:
            usuario.delete()

            return Response({
                "detail": f'Usuário {nome_usuario} excluído com sucesso.'},
                status=status.HTTP_200_OK    
            )

        except Exception as e:
            return Response(
                {"detail": "Erro na exclusão do usuário",
                 "error": f"Erro na exclusão: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )





class ProdutoViewSet(viewsets.GenericViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="listar-produtos",
        url_name="listar-produtos"
    )
    def listar_produtos(self, request):

        if self.queryset:

            produtos = []
            for item in self.queryset:
                produtos.append({
                    "id": item.id,
                    "titulo": item.titulo,
                    "descricao": item.descricao,
                    "preço": item.preco,
                    "urlImagem": item.url_imagem,
                    "categoria_id": item.categoria.id,
                    "categoria": item.categoria.nome,
                    "usuario_id": item.usuario.id,
                    "anunciante": item.usuario.nome
                })
            
            return Response(
                produtos,
                status=status.HTTP_200_OK
            )
        
        return Response({
            "detail": "Não foram encontrados produtos."},
            status=status.HTTP_404_NOT_FOUND
        )
    

    @extend_schema(
        request=ProdutoSerializer,
        responses={201: ProdutoSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="cadastrar-produto",
        url_name="cadastrar-produto"
    )
    def cadastrar_produto(self, request):
        dados = request.data

        titulo = dados.get('titulo')
        descricao = dados.get('descricao')
        preco = dados.get('preco')
        url_imagem = dados.get('url_imagem')        
        usuario = dados.get('usuario')
        categoria = dados.get('categoria')

        if all([titulo, descricao, preco, url_imagem, usuario, categoria]):
            
            serializer = self.get_serializer(data=dados)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        
        return Response(
            {"detail": "Faltam o preenchimento de campos obrigatórios"},
            status=status.HTTP_400_BAD_REQUEST
        )
    





