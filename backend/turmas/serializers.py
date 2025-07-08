from rest_framework import serializers
from .models import Turma, Atividade
from usuarios.models import Usuario 

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'


    def validate_professor(self, value):
        if value.tipo != 'professor':
            raise serializers.ValidationError("O usuário selecionado não é um professor.")
        return value

class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = '__all__'
