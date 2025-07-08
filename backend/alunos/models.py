from django.db import models
from usuarios.models import Usuario

class Aluno(models.Model):
    id = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id'  # 👈 isso resolve o problema do "id_id"
    )
    matricula = models.CharField(max_length=20, unique=True)
    periodo_ingresso = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'alunos'

    def __str__(self):
        return f"{self.matricula} - {self.id.nome}"
