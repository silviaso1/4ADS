from rest_framework import serializers
from .models import Matricula, Nota, PeriodoMatricula

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'

    def validate_aluno(self, value):
        if value.tipo != 'aluno':
            raise serializers.ValidationError("Somente usuários do tipo 'aluno' podem ser matriculados.")
        return value

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'

    def validate_aluno(self, value):
        if value.tipo != 'aluno':
            raise serializers.ValidationError("Apenas alunos podem receber notas.")
        return value

class PeriodoMatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoMatricula
        fields = '__all__'
