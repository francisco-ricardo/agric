"""
urls.py

Configuração das rotas da API do app Agric.

Este módulo define as URLs públicas da aplicação, expondo os endpoints RESTful para:
- Produtores
- Estados
- Cidades
- Tipos de Cultura
- Propriedades
- Culturas
- Dashboard consolidado

As rotas seguem o padrão REST, utilizando o DefaultRouter do Django REST Framework 
para os recursos principais, e uma rota customizada para o dashboard.

Rotas principais:
- /admin/                : Interface administrativa do Django.
- /api/produtores/       : CRUD de produtores rurais.
- /api/estados/          : CRUD de estados.
- /api/cidades/          : CRUD de cidades.
- /api/tipos-cultura/    : CRUD de tipos de cultura.
- /api/propriedades/     : CRUD de propriedades rurais.
- /api/culturas/         : CRUD de culturas agrícolas.
- /api/dashboard/        : Visão consolidada dos dados (dashboard).
"""
from django.contrib import admin
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutorViewSet
from .views import EstadoViewSet
from .views import CidadeViewSet
from .views import TipoCulturaViewSet
from .views import PropriedadeViewSet
from .views import CulturaViewSet
from .views import DashboardView


router = DefaultRouter()
router.register(r'produtores', ProdutorViewSet, basename='produtor')
router.register(r'estados', EstadoViewSet, basename='estado')
router.register(r'cidades', CidadeViewSet, basename='cidade')
router.register(r'tipos-cultura', TipoCulturaViewSet, basename='tipocultura')
router.register(r'propriedades', PropriedadeViewSet, basename='propriedade')
router.register(r'culturas', CulturaViewSet, basename='cultura')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
]
