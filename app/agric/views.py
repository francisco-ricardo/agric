"""
views.py

Este módulo define as views da API REST para o app Agric, utilizando Django REST Framework.

Inclui ViewSets para os principais recursos do domínio agrícola:
- Produtor
- Estado
- Cidade
- TipoCultura
- Propriedade
- Cultura

Cada ViewSet provê operações CRUD completas, com suporte a filtros por identificadores 
customizados (ex: cpf_cnpj, id_estado, etc).
Também expõe um endpoint customizado para o dashboard consolidado, que retorna estatísticas 
agregadas sobre fazendas, culturas e uso do solo.

Classes:
- ProdutorViewSet: CRUD de produtores rurais.
- EstadoViewSet: CRUD de estados.
- CidadeViewSet: CRUD de cidades.
- TipoCulturaViewSet: CRUD de tipos de cultura.
- PropriedadeViewSet: CRUD de propriedades rurais.
- CulturaViewSet: CRUD de culturas agrícolas.
- DashboardView: Endpoint GET para estatísticas consolidadas.
"""

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Sum, Count

from .models import Produtor
from .serializers import ProdutorSerializer
from .models import Estado
from .serializers import EstadoSerializer
from .models import Cidade
from .serializers import CidadeSerializer
from .models import TipoCultura
from .serializers import TipoCulturaSerializer
from .models import Cultura
from .serializers import CulturaSerializer
from .models import Propriedade
from .serializers import PropriedadeSerializer


class ProdutorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Produtor.

    Permite listar, criar, atualizar e deletar produtores rurais.
    Utiliza o campo 'cpf_cnpj' como identificador principal nas rotas.
    """
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer
    lookup_field = 'cpf_cnpj'


class EstadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Estado.

    Permite listar, criar, atualizar e deletar estados.
    Utiliza o campo 'id_estado' como identificador principal nas rotas.
    """
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    lookup_field = 'id_estado'


class CidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Cidade.

    Permite listar, criar, atualizar e deletar cidades.
    Utiliza o campo 'id_cidade' como identificador principal nas rotas.
    """
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    lookup_field = 'id_cidade'


class TipoCulturaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de TipoCultura.

    Permite listar, criar, atualizar e deletar tipos de cultura agrícola.
    Utiliza o campo 'id_tipo_cultura' como identificador principal nas rotas.
    """
    queryset = TipoCultura.objects.all()
    serializer_class = TipoCulturaSerializer
    lookup_field = 'id_tipo_cultura'


class PropriedadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Propriedade.

    Permite listar, criar, atualizar e deletar propriedades rurais.
    Utiliza o campo 'id_propriedade' como identificador principal nas rotas.
    """
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer
    lookup_field = 'id_propriedade'


class CulturaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Cultura.

    Permite listar, criar, atualizar e deletar culturas agrícolas.
    Utiliza o campo 'id_cultura' como identificador principal nas rotas.
    """
    queryset = Cultura.objects.all()
    serializer_class = CulturaSerializer
    lookup_field = 'id_cultura'


class DashboardView(APIView):
    """
    Endpoint somente leitura para estatísticas consolidadas do sistema.

    Retorna dados agregados sobre fazendas, hectares, culturas plantadas,
    distribuição por estado e uso do solo.
    Disponível apenas via método GET.
    """
    def get(self, request):
        # Total de fazendas cadastradas
        total_fazendas = Propriedade.objects.count()
        # Total de hectares registrados (área total)
        total_hectares = Propriedade.objects.aggregate(total=Sum('area_total'))['total'] or 0

        # Gráfico de pizza: por estado
        fazendas_por_estado = (
            Propriedade.objects
                .values(nome_estado=F('cidade__estado__nome_estado'))
                .annotate(
                    qtd_fazendas=Count('id_propriedade'),
                    total_hectares=Sum('area_total')
                )
                .order_by('-qtd_fazendas')
        )

        # Gráfico de pizza: por cultura plantada
        culturas = (
            Cultura.objects
                .values(nome_tipo_cultura=F('tipo_cultura__tipo_cultura'))
                .annotate(qtd=Count('id_cultura'))
                .order_by('-qtd')
        )   
        culturas_list = []
        for item in culturas:
            item['tipo_cultura'] = item.pop('nome_tipo_cultura')
            culturas_list.append(item)

        # Gráfico de pizza: uso do solo
        uso_solo = Propriedade.objects.aggregate(
            total_agricultavel=Sum('area_agricultavel'),
            total_vegetacao=Sum('area_vegetacao')
        )

        return Response({
            "total_fazendas": total_fazendas,
            "total_hectares": total_hectares,
            "fazendas_por_estado": list(fazendas_por_estado),
            "culturas_plantadas": culturas_list,
            "uso_do_solo": uso_solo,
        }, status=status.HTTP_200_OK)
