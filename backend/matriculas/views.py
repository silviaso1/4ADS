from rest_framework import viewsets
from django.db.models import Avg
from .models import Matricula, Nota, PeriodoMatricula
from .serializers import MatriculaSerializer, NotaSerializer, PeriodoMatriculaSerializer

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

    def perform_create(self, serializer):
        nota = serializer.save()

       
        media = Nota.objects.filter(
            aluno=nota.aluno,
            turma=nota.turma
        ).aggregate(avg_nota=Avg('nota'))['avg_nota']

        try:
            matricula = Matricula.objects.get(aluno=nota.aluno, turma=nota.turma)
            matricula.media_final = media
            matricula.save()
        except Matricula.DoesNotExist:
            pass 

class PeriodoMatriculaViewSet(viewsets.ModelViewSet):
    queryset = PeriodoMatricula.objects.all()
    serializer_class = PeriodoMatriculaSerializer
