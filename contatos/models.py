from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(
        default=timezone.now)
    descricao = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)
    foto = models.ImageField(blank=True, upload_to='fotos/%y/%m/%d')

    def __str__(self):
        return self.nome
