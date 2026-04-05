from django.db import models
from usuarios.models import Usuario
from categorias.models import Categoria

# Create your models here.
class Produto(models.Model):
    titulo = models.CharField(verbose_name='Titulo', max_length=100)
    descricao = models.CharField(verbose_name='Descricao', max_length=200, blank=True)
    preco = models.DecimalField(verbose_name='Preço', max_digits=10, decimal_places=2)
    url_imagem = models.CharField(verbose_name='Url_Imagem', max_length=300)
    usuario = models.ForeignKey(
        Usuario, verbose_name="Usuario_Id", on_delete=models.CASCADE
    )
    categoria = models.ForeignKey(
        Categoria, verbose_name="Categoria_Id", on_delete=models.CASCADE
    )

    class Meta:
        db_table = u'produto'
        managed= True
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

    def __str__(self):
        return '%s / %s / %s / %s / %s / %s' % (self.titulo, self.descricao, self.preco, self.url_imagem, self.usuario, self.categoria)