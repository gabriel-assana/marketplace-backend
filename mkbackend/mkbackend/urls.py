"""
URL configuration for mkbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from mkbackend import views
# from mkbackend.views import (CategoriaViewSet, UsuarioViewSet, ProdutoViewSet)

app_name = 'mk_backend'
router = routers.DefaultRouter()


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# router.register(r"PSA", PsaViewSet, basename="psa")
router.register(r"categoria", views.CategoriaViewSet, basename="categoria")
router.register(r"usuario", views.UsuarioViewSet, basename="usuario")
router.register(r"produto", views.ProdutoViewSet, basename="produto")


urlpatterns = [
    # path('api/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # path('ilab/', views.IlabApiView.as_view(), name="ilab")

    # path('categoria/', views.CategoriaViewSet.as_view(), name="categoria")
]
