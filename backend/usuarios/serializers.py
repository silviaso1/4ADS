from rest_framework import serializers
from .models import Usuario
from alunos.models import Aluno  # Ajuste conforme seu projeto
from datetime import date

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha', 'tipo', 'token']
        extra_kwargs = {
            'token': {'read_only': True},
            'senha': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        usuario = super().create(validated_data)

        # Criar Aluno se for tipo aluno
        if usuario.tipo == 'aluno':
            ano = date.today().year
            mes = date.today().month
            semestre = 1 if mes <= 6 else 2
            periodo = f"{ano}.{semestre}"

            matricula = f"ALU{ano}{usuario.id:04d}"  # Ex: ALU20250001

            Aluno.objects.create(
            id=usuario,  
            matricula=matricula,
            periodo_ingresso=periodo
)

        return usuario
