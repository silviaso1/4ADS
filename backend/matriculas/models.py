from django.db import models
from usuarios.models import Usuario
from turmas.models import Turma, Atividade

class Matricula(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='aluno_id')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, blank=True, null=True)
    media_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'matriculas'
        unique_together = ('aluno', 'turma')

    def __str__(self):
        return f'{self.aluno.nome} - {self.turma.nome}'


class Nota(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='aluno_id')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'notas'
        unique_together = ('aluno', 'atividade')

    def __str__(self):
        return f'{self.aluno.nome} - {self.atividade.nome}: {self.nota}'


class PeriodoMatricula(models.Model):
    inicio = models.DateField()
    fim = models.DateField()
    aberto = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'periodo_matricula'

    def __str__(self):
        return f'{self.inicio} a {self.fim}'
