from django.db import models

class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=1)

    class Meta:
        abstract = True

# Create your models here.
class Usuario(Base):
    nome = models.CharField(verbose_name='Nome', max_length=100)
    email = models.EmailField(verbose_name='Email', max_length=100, unique=True)
    senha = models.CharField(max_length=255)
    super_user = models.SmallIntegerField(default=0)
    cpf = models.BigIntegerField(verbose_name='Cpf', max_length=11, unique=True)

    class Meta:
        db_table = u'usuario'
        managed= True
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return '%s / %s / %s / %s' % (self.nome, self.email, self.super_user, self.cpf)