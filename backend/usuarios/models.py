from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(models.Model):
    TIPO_CHOICES = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Administrador'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    token = models.CharField(max_length=255, blank=True, null=True)  # <--- Adiciona isso aqui

    class Meta:
        managed = False
        db_table = 'usuarios'

    def __str__(self):
        return self.nome