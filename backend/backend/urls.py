from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/usuarios/', include('usuarios.urls')),
    path('api/alunos/', include('alunos.urls')),
    path('api/turmas/', include('turmas.urls')),
    path('api/matriculas/', include('matriculas.urls')),
]
