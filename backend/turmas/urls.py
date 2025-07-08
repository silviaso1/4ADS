from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TurmaViewSet, AtividadeViewSet

router = DefaultRouter()
router.register(r'atividades', AtividadeViewSet)
router.register(r'', TurmaViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
