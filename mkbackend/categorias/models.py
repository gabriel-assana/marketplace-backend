from django.db import models


class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=1)

    class Meta:
        abstract = True



# Create your models here.
class Categoria(Base):
    nome = models.CharField(verbose_name='Nome', max_length=100)

    class Meta:
        db_table = u'categoria'
        managed= True
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nome
        # return '%s / %s' % (self.nome)