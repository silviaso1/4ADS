from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario
from .serializers import UsuarioSerializer
import secrets

# 🔐 Nova permissão baseada em token manual
class IsAdminWithToken(permissions.BasePermission):
    """
    Permite apenas se o token for válido e o usuário for admin.
    """
    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        if not token:
            return False
        user = Usuario.objects.filter(token=token).first()
        if user and user.tipo == 'admin':
            request.user = user  # Define o user manualmente
            return True
        return False

# 🔧 Cadastro de usuários (protegido com IsAdminWithToken)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminWithToken]

    def perform_create(self, serializer):
        senha = "4ADS123"  # senha fixa
        usuario = serializer.save(senha=senha)
        # Enviar email simulado
        send_mail(
            subject="Cadastro no sistema",
            message=f"Bem-vindo!\n\nLogin: {usuario.email}\nSenha: {senha}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=False,
        )

# 🔑 Login com geração de token
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    senha = request.data.get('senha')
    user = Usuario.objects.filter(email=email, senha=senha).first()
    if user:
        # Gera e salva um token aleatório
        token = secrets.token_hex(20)
        user.token = token
        user.save()
        return Response({
            "mensagem": "Login bem-sucedido",
            "token": token,
            "tipo": user.tipo
        }, status=200)
    return Response({"mensagem": "Credenciais inválidas"}, status=401)
