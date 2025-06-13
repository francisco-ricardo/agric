"""
URL configuration for agric project.

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
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutorViewSet
from .views import EstadoViewSet
from .views import CidadeViewSet

router = DefaultRouter()

router.register(r'produtores', ProdutorViewSet, basename='produtor')
router.register(r'estados', EstadoViewSet, basename='estado')
router.register(r'cidades', CidadeViewSet, basename='cidade')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
