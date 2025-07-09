from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario
from .serializers import UsuarioSerializer
import secrets


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        tipo = serializer.validated_data.get('tipo')

        if tipo == 'professor':
            senha = "AV24ADS20255"
        else:
            senha = "4ADS123"

        usuario = serializer.save(senha=senha)

    
        send_mail(
            subject="Cadastro no sistema",
            message=f"Bem-vindo!\n\nLogin: {usuario.email}\nSenha: {senha}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=False,
        )


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    senha = request.data.get('senha')

    user = Usuario.objects.filter(email=email, senha=senha).first()
    if user:
        return Response({
            "mensagem": "Login bem-sucedido",
            "tipo": user.tipo,
            "nome": user.nome
        }, status=200)
    
    return Response({"mensagem": "Credenciais inválidas"}, status=401)
