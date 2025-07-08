from django.db import models
from usuarios.models import Usuario

class Turma(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    periodo = models.CharField(max_length=20, blank=True, null=True)
    horario = models.CharField(max_length=50, blank=True, null=True)
    sala = models.CharField(max_length=50, blank=True, null=True)
    professor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, db_column='professor_id')

    class Meta:
        managed = False
        db_table = 'turmas'

    def __str__(self):
        return self.nome


class Atividade(models.Model):
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'atividades'

    def __str__(self):
        return self.nome
