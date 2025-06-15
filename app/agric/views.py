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

import logging
logger = logging.getLogger(__name__)


class LoggingModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet base com logging centralizado para operações CRUD.
    """
    def list(self, request, *args, **kwargs):
        logger.info("Listagem de %s acessada por %s", self.__class__.__name__, request.user)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Tentativa de criação em %s por %s", self.__class__.__name__, request.user)
        try:
            response = super().create(request, *args, **kwargs)
            logger.info("%s criado com sucesso: %s", self.__class__.__name__, response.data)
            return response
        except Exception as e:
            logger.error("Erro ao criar em %s: %s", self.__class__.__name__, str(e), exc_info=True)
            raise

    def update(self, request, *args, **kwargs):
        logger.info("Tentativa de atualização em %s por %s", self.__class__.__name__, request.user)
        try:
            response = super().update(request, *args, **kwargs)
            logger.info("%s atualizado: %s", self.__class__.__name__, response.data)
            return response
        except Exception as e:
            logger.error("Erro ao atualizar em %s: %s", self.__class__.__name__, str(e), exc_info=True)
            raise

    def destroy(self, request, *args, **kwargs):
        logger.info("Tentativa de deleção em %s por %s", self.__class__.__name__, request.user)
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info("%s deletado: id=%s", self.__class__.__name__, kwargs.get(self.lookup_field))
            return response
        except Exception as e:
            logger.error("Erro ao deletar em %s: %s", self.__class__.__name__, str(e), exc_info=True)
            raise

class ProdutorViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de Produtor.
    """
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer
    lookup_field = 'cpf_cnpj'

class EstadoViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de Estado.
    """
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    lookup_field = 'id_estado'

class CidadeViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de Cidade.
    """
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    lookup_field = 'id_cidade'

class TipoCulturaViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de TipoCultura.
    """
    queryset = TipoCultura.objects.all()
    serializer_class = TipoCulturaSerializer
    lookup_field = 'id_tipo_cultura'

class PropriedadeViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de Propriedade.
    """
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer
    lookup_field = 'id_propriedade'

class CulturaViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de Cultura.
    """
    queryset = Cultura.objects.all()
    serializer_class = CulturaSerializer
    lookup_field = 'id_cultura'

class DashboardView(APIView):
    """
    Endpoint somente leitura para estatísticas consolidadas do sistema.
    """
    def get(self, request):
        logger.info("Dashboard acessado por %s", request.user)
        try:
            total_fazendas = Propriedade.objects.count()
            total_hectares = Propriedade.objects.aggregate(total=Sum('area_total'))['total'] or 0

            fazendas_por_estado = (
                Propriedade.objects
                    .values(nome_estado=F('cidade__estado__nome_estado'))
                    .annotate(
                        qtd_fazendas=Count('id_propriedade'),
                        total_hectares=Sum('area_total')
                    )
                    .order_by('-qtd_fazendas')
            )

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

            uso_solo = Propriedade.objects.aggregate(
                total_agricultavel=Sum('area_agricultavel'),
                total_vegetacao=Sum('area_vegetacao')
            )

            data = {
                "total_fazendas": total_fazendas,
                "total_hectares": total_hectares,
                "fazendas_por_estado": list(fazendas_por_estado),
                "culturas_plantadas": culturas_list,
                "uso_do_solo": uso_solo,
            }
            logger.debug("Dados do dashboard: %s", data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Erro ao calcular estatísticas do dashboard: %s", str(e), exc_info=True)
            return Response({"detail": "Erro interno ao calcular dashboard."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

