from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings  # Importa as configurações

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('plataforma/', include('plataforma.urls')),
    path('gestao_comercial/', include('gestao_comercial.urls')),
    path('', include('usuarios.urls'))
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)