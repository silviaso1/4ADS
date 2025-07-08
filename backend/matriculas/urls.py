from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatriculaViewSet, NotaViewSet, PeriodoMatriculaViewSet

router = DefaultRouter()
router.register(r'notas', NotaViewSet)
router.register(r'periodos', PeriodoMatriculaViewSet)
router.register(r'', MatriculaViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
