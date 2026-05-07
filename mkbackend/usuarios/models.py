from django.db import models
from django.contrib.auth.hashers import make_password, identify_hasher
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=1)

    class Meta:
        abstract = True

# O Django precisa de um "Manager" para saber como criar usuários no terminal (createsuperuser)
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, cpf, password=None):
        if not email:
            raise ValueError('Usuário deve ter um e-mail')
        user = self.model(email=self.normalize_email(email), nome=nome, cpf=cpf)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, cpf, password=None):
        user = self.create_user(email, nome, cpf, password)
        user.super_user = 1
        user.save(using=self._db)
        return user

# Create your models here.
class Usuario(AbstractBaseUser, Base): # Herança dupla: Auth + sua base
    nome = models.CharField(verbose_name='Nome', max_length=100)
    email = models.EmailField(verbose_name='Email', max_length=100, unique=True)
    senha = models.CharField(max_length=255)
    super_user = models.SmallIntegerField(default=0)
    cpf = models.BigIntegerField(verbose_name='Cpf', max_length=11, unique=True)
    status = models.SmallIntegerField(default=1)

    objects = UsuarioManager()

    # Configurações Obrigatórias para Auth
    USERNAME_FIELD = 'email'    # Campo usado para login
    REQUIRED_FIELDS = ['nome', 'cpf'] # Campos pedidos no createsuperuser

    class Meta:
        db_table = u'usuario'
        managed= True
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    @property
    def is_active(self):
        # O SimpleJWT olha para esta propriedade
        return self.status == 1

    # Métodos necessários para o Django Admin (se você for usar)
    @property
    def is_staff(self):
        return self.super_user == 1

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # Substituímos o password manual pelo padrão do Django
    @property
    def password(self):
        return self.senha
    
    @password.setter
    def password(self, value):
        self.senha = value

    def save(self, *args, **kwargs):
        # Verifica se a senha já é um hash. Se não for, criptografa.
        try:
            identify_hasher(self.senha)
        except ValueError:
            self.senha = make_password(self.senha)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s / %s / %s / %s' % (self.nome, self.email, self.super_user, self.cpf)