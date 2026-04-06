from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework import viewsets, status, filters
from usuarios.models import Usuario
from categorias.models import Categoria
from produtos.models import Produto

from usuarios.serializers import UsuarioSerializer, CadastroUsuarioSerializer
from categorias.serializers import CategoriaSerializer, CadastrarCategoriaSerializer
from produtos.serializers import ProdutoSerializer, CadastrarProdutoSerializer

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
            "categoria": categoria.nome,
            "status": categoria.status,
            "criacao": categoria.criacao,
            "atualizacao": categoria.atualizacao
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
        request=CadastrarCategoriaSerializer,
        responses={201: CadastrarCategoriaSerializer}
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
        url_path="editar-categoria",
        url_name="editar-categoria"
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


    # @action(
    #     detail=True,
    #     methods=["delete"],
    #     url_path="excluir_categoria",
    #     url_name="excluir_categoria"
    # )
    # def excluir_categoria(self, request, pk=None):

    #     categoria = Categoria.objects.filter(pk=pk).first()

    #     if not categoria:
    #         return Response(
    #             {"detail": "Categoria não encontrada ou já foi excluída."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )

    #     nome_categoria = categoria.nome

    #     try:
    #         categoria.delete()
        
    #         return Response({
    #             "detail": f'Categoria {nome_categoria} excluída com sucesso.'},
    #             status=status.HTTP_200_OK    
    #         )
        
    #     except Exception as e:
    #         return Response(
    #             {"detail": "Erro na exclusão da categoria",
    #              "error": f"Erro na exclusão: {str(e)}"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    
    @extend_schema(
        request=None, # Não exige corpo na requisição
        responses={200: OpenApiTypes.STR}
    )
    @action(
        detail=True,
        methods=["put"],
        url_path="excluir-categoria", # Nome mais semântico para a função
        url_name="excluir-categoria"
    )
    def excluir_categoria(self, request, pk=None):
        # 1. Obtém a instância da categoria pelo ID (pk)
        instance = self.get_object()

        estado = 'excluída'

        # 2. Altera apenas o campo status
        if instance.status == 0:
            instance.status = 1
            estado = 'ativada'
        else:
            instance.status = 0
        
        # 3. Salva no banco (o campo 'atualizacao' será atualizado pelo auto_now=True)
        instance.save()

        return Response(
            {"detail": f"Categoria '{instance.nome}' {estado} com sucesso."},
            status=status.HTTP_200_OK
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


    @action(
        detail=True,
        methods=["get"],
        url_path="buscar-usurioid",
        url_name="buscar-usurioid"
    )
    def buscar_usuarioid(self, request, pk=None):

        usuario = get_object_or_404(Usuario, pk=pk)

        if not usuario:
            return Response(
                {"detail": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "super_user": usuario.super_user,
            "cpf": usuario.cpf,
            "status": usuario.status,
            "criacao": usuario.criacao,
            "atualizacao": usuario.atualizacao
        }

        return Response(
            serializer,
            status=status.HTTP_200_OK
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
        responses={200: UsuarioSerializer}
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


    # @action(
    #     detail=True,
    #     methods=["delete"],
    #     url_path="excluir-usuario",
    #     url_name="excluir-usuario"
    # )
    # def excluir_usuario(self, request, pk=None):

    #     usuario = Usuario.objects.filter(pk=pk).first()

    #     if not usuario:
    #         return Response(
    #             {"detail": "Usuário não encontrado ou já foi excluído."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
        
    #     nome_usuario = usuario.nome

    #     try:
    #         usuario.delete()

    #         return Response({
    #             "detail": f'Usuário {nome_usuario} excluído com sucesso.'},
    #             status=status.HTTP_200_OK    
    #         )

    #     except Exception as e:
    #         return Response(
    #             {"detail": "Erro na exclusão do usuário",
    #              "error": f"Erro na exclusão: {str(e)}"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )


    @extend_schema(
        request=None, # Não exige corpo na requisição
        responses={200: OpenApiTypes.STR}
    )
    @action(
        detail=True,
        methods=["put"],
        url_path="excluir-usuario", # Nome mais semântico para a função
        url_name="excluir-usuario"
    )
    def excluir_usuario(self, request, pk=None):
        # 1. Obtém a instância da categoria pelo ID (pk)
        instance = self.get_object()

        estado = 'excluído'

        # 2. Altera apenas o campo status
        if instance.status == 0:
            instance.status = 1
            estado = 'ativado'
        else:
            instance.status = 0
        
        # 3. Salva no banco (o campo 'atualizacao' será atualizado pelo auto_now=True)
        instance.save()

        return Response(
            {"detail": f"Usuario '{instance.nome}' {estado} com sucesso."},
            status=status.HTTP_200_OK
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
                    "usuario": item.usuario.nome,
                    "status": item.status,
                    "criacao": item.criacao,
                    "atualizacao": item.atualizacao,
                })
            
            return Response(
                produtos,
                status=status.HTTP_200_OK
            )
        
        return Response({
            "detail": "Não foram encontrados produtos."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(
        detail=True,
        methods=["get"],
        url_path="buscar-produtoid",
        url_name="buscar-produtoid"
    )
    def buscar_produtoid(self, request, pk=None):

        produto = get_object_or_404(Produto, pk=pk)

        if not produto:
            return Response(
                {"detail": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = {
            "titulo": produto.titulo,
            "descricao": produto.descricao,
            "preco": produto.preco,
            "url_imagem": produto.url_imagem,            
            "categoria_id": produto.categoria.id,
            "categoria": produto.categoria.nome,
            "usuario_id": produto.usuario.id,
            "usuario": produto.usuario.nome,
            "status": produto.status,
            "criacao": produto.criacao,
            "atualizacao": produto.atualizacao,
        }

        return Response(
            serializer,
            status=status.HTTP_200_OK
        )


    @extend_schema(
        request=CadastrarProdutoSerializer,
        responses={201: CadastrarProdutoSerializer}
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
    

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='titulo', 
                description='Título do produto para busca', 
                required=True, 
                type=OpenApiTypes.STR
            ),
        ],
        responses={200: ProdutoSerializer}
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="buscar-produto",
        url_name="buscar-produto"
    )
    def buscar_produto(self, request):

        """Busca o produto somente pelo título."""

        nome_produto = request.query_params.get('titulo', None)

        if nome_produto is not None:
            produtos = Produto.objects.filter(titulo__icontains=nome_produto)

            serializer = self.get_serializer(produtos, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"detail": "O parâmetro 'título' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST
        )


    @action(
        detail=True,
        methods=["put"],
        url_path="editar-produto",
        url_name="editar-produto"
    )
    def editar_produto(self, request, pk=None):

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


    # @action(
    #     detail=True,
    #     methods=["delete"],
    #     url_path="excluir-produto",
    #     url_name="excluir-produto"
    # )
    # def excluir_produto(self, request, pk=None):

    #     produto = Produto.objects.filter(pk=pk).first()

    #     if not produto:
    #         return Response(
    #             {"detail": "Produto não encontrado ou já foi excluído."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
        
    #     nome_produto = produto.titulo

    #     try:
    #         produto.delete()

    #         return Response({
    #             "detail": f'Produto {nome_produto} excluído com sucesso.'},
    #             status=status.HTTP_200_OK    
    #         )

    #     except Exception as e:
    #         return Response(
    #             {"detail": "Erro na exclusão do produto",
    #              "error": f"Erro na exclusão: {str(e)}"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )


    @extend_schema(
        request=None, # Não exige corpo na requisição
        responses={200: OpenApiTypes.STR}
    )
    @action(
        detail=True,
        methods=["put"],
        url_path="excluir-produto", # Nome mais semântico para a função
        url_name="excluir-produto"
    )
    def produto_usuario(self, request, pk=None):
        # 1. Obtém a instância da categoria pelo ID (pk)
        instance = self.get_object()

        estado = 'excluído'

        # 2. Altera apenas o campo status
        if instance.status == 0:
            instance.status = 1
            estado = 'ativado'
        else:
            instance.status = 0
        
        # 3. Salva no banco (o campo 'atualizacao' será atualizado pelo auto_now=True)
        instance.save()

        return Response(
            {"detail": f"Produto '{instance.titulo}' {estado} com sucesso."},
            status=status.HTTP_200_OK
        )






