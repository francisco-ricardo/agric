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
import time

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

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiExample

import logging
logger = logging.getLogger(__name__)


class LoggingModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet base com logging de tempo de execução, usuário e tratamento de exceções 
    para operações CRUD.
    """
    def list(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        start = time.monotonic()
        response = super().list(request, *args, **kwargs)
        elapsed = time.monotonic() - start
        logger.info("Usuário %s acessou list %s | Tempo: %.3fs", user, self.__class__.__name__, elapsed)
        return response

    def create(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        start = time.monotonic()
        try:
            response = super().create(request, *args, **kwargs)
            logger.info("Usuário %s criou em %s | Tempo: %.3fs", user, self.__class__.__name__, time.monotonic() - start)
            return response
        except Exception as e:
            elapsed = time.monotonic() - start
            logger.error("Erro ao criar em %s por %s: %s | Tempo: %.3fs", self.__class__.__name__, user, str(e), elapsed, exc_info=True)
            raise

    def update(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        start = time.monotonic()
        try:
            response = super().update(request, *args, **kwargs)
            logger.info("Usuário %s atualizou em %s | Tempo: %.3fs", user, self.__class__.__name__, time.monotonic() - start)
            return response
        except Exception as e:
            elapsed = time.monotonic() - start
            logger.error("Erro ao atualizar em %s por %s: %s | Tempo: %.3fs", self.__class__.__name__, user, str(e), elapsed, exc_info=True)
            raise


    def partial_update(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        start = time.monotonic()
        try:
            response = super().partial_update(request, *args, **kwargs)
            logger.info("Usuário %s fez PATCH em %s | Tempo: %.3fs", user, self.__class__.__name__, time.monotonic() - start)
            return response
        except Exception as e:
            elapsed = time.monotonic() - start
            logger.error("Erro ao fazer PATCH em %s por %s: %s | Tempo: %.3fs", self.__class__.__name__, user, str(e), elapsed, exc_info=True)
            raise


    def destroy(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        start = time.monotonic()
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info("Usuário %s deletou em %s | Tempo: %.3fs", user, self.__class__.__name__, time.monotonic() - start)
            return response
        except Exception as e:
            elapsed = time.monotonic() - start
            logger.error("Erro ao deletar em %s por %s: %s | Tempo: %.3fs", self.__class__.__name__, user, str(e), elapsed, exc_info=True)
            raise


@extend_schema_view(
    list=extend_schema(
        summary="Listar produtores",
        description="Retorna uma lista paginada de produtores rurais cadastrados no sistema.",
        responses={200: ProdutorSerializer(many=True)},
        examples=[
            OpenApiExample(
                'Exemplo de resposta',
                value=[
                    {"cpf_cnpj": "12345678901", "tipo_documento": "CPF", "nome_produtor": "João Silva"},
                    {"cpf_cnpj": "12345678000199", "tipo_documento": "CNPJ", "nome_produtor": "Fazenda Boa Terra"}
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Criar produtor",
        description="Cria um novo produtor rural. O campo `cpf_cnpj` deve ser único e válido (CPF ou CNPJ).",
        request=ProdutorSerializer,
        responses={201: ProdutorSerializer},
        examples=[
            OpenApiExample(
                'Exemplo de requisição',
                value={"cpf_cnpj": "12345678901", "nome_produtor": "João Silva"},
                request_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Detalhar produtor",
        description="Retorna os dados de um produtor rural identificado por CPF ou CNPJ.",
        responses={200: ProdutorSerializer}
    ),
    update=extend_schema(
        summary="Atualizar produtor",
        description="Atualiza os dados de um produtor rural existente.",
        request=ProdutorSerializer,
        responses={200: ProdutorSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de produtor",
        description="Atualiza parcialmente os dados de um produtor rural. Apenas os campos enviados serão alterados.",
        request=ProdutorSerializer,
        responses={200: ProdutorSerializer}
    ),
    destroy=extend_schema(
        summary="Deletar produtor",
        description="Remove um produtor rural do sistema.",
        responses={204: None}
    ),
)
class ProdutorViewSet(LoggingModelViewSet):
    """
    Endpoints para gestão de produtores rurais.

    Permite listar, criar, consultar, atualizar e deletar produtores.
    O campo `cpf_cnpj` pode ser CPF ou CNPJ, e é usado como identificador único.
    """
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer
    lookup_field = 'cpf_cnpj'


@extend_schema_view(
    list=extend_schema(
        summary="Listar estados",
        description="Retorna todos os estados cadastrados.",
        responses={200: EstadoSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar estado",
        description="Cria um novo estado.",
        request=EstadoSerializer,
        responses={201: EstadoSerializer}
    ),
    retrieve=extend_schema(
        summary="Detalhar estado",
        description="Retorna os dados de um estado pelo seu ID.",
        responses={200: EstadoSerializer}
    ),
    update=extend_schema(
        summary="Atualizar estado",
        description="Atualiza os dados de um estado existente.",
        request=EstadoSerializer,
        responses={200: EstadoSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de estado",
        description="Atualiza parcialmente os dados de um estado. Apenas os campos enviados serão alterados.",
        request=EstadoSerializer,
        responses={200: EstadoSerializer}
    ),
    destroy=extend_schema(
        summary="Deletar estado",
        description="Remove um estado do sistema.",
        responses={204: None}
    ),
)
class EstadoViewSet(LoggingModelViewSet):
    """
    Endpoints para gestão de estados.
    """
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    lookup_field = 'id_estado'


@extend_schema_view(
    list=extend_schema(
        summary="Listar cidades",
        description="Retorna todas as cidades cadastradas.",
        responses={200: CidadeSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar cidade",
        description="Cria uma nova cidade vinculada a um estado.",
        request=CidadeSerializer,
        responses={201: CidadeSerializer}
    ),
    retrieve=extend_schema(
        summary="Detalhar cidade",
        description="Retorna os dados de uma cidade pelo seu ID.",
        responses={200: CidadeSerializer}
    ),
    update=extend_schema(
        summary="Atualizar cidade",
        description="Atualiza os dados de uma cidade existente.",
        request=CidadeSerializer,
        responses={200: CidadeSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de cidade",
        description="Atualiza parcialmente os dados de uma cidade. Apenas os campos enviados serão alterados.",
        request=CidadeSerializer,
        responses={200: CidadeSerializer}
    ),
    destroy=extend_schema(
        summary="Deletar cidade",
        description="Remove uma cidade do sistema.",
        responses={204: None}
    ),
)
class CidadeViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de Cidade.
    """
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    lookup_field = 'id_cidade'


@extend_schema_view(
    list=extend_schema(
        summary="Listar tipos de cultura",
        description="Retorna todos os tipos de cultura agrícola cadastrados.",
        responses={200: TipoCulturaSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar tipo de cultura",
        description="Cria um novo tipo de cultura agrícola.",
        request=TipoCulturaSerializer,
        responses={201: TipoCulturaSerializer}
    ),
    retrieve=extend_schema(
        summary="Detalhar tipo de cultura",
        description="Retorna os dados de um tipo de cultura pelo seu ID.",
        responses={200: TipoCulturaSerializer}
    ),
    update=extend_schema(
        summary="Atualizar tipo de cultura",
        description="Atualiza os dados de um tipo de cultura existente.",
        request=TipoCulturaSerializer,
        responses={200: TipoCulturaSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de tipo de cultura",
        description="Atualiza parcialmente os dados de um tipo de cultura. Apenas os campos enviados serão alterados.",
        request=TipoCulturaSerializer,
        responses={200: TipoCulturaSerializer}
    ),
    destroy=extend_schema(
        summary="Deletar tipo de cultura",
        description="Remove um tipo de cultura do sistema.",
        responses={204: None}
    ),
)
class TipoCulturaViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de TipoCultura.
    """
    queryset = TipoCultura.objects.all()
    serializer_class = TipoCulturaSerializer
    lookup_field = 'id_tipo_cultura'


@extend_schema_view(
    list=extend_schema(
        summary="Listar propriedades",
        description="Retorna todas as propriedades rurais cadastradas.",
        responses={200: PropriedadeSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar propriedade",
        description="Cria uma nova propriedade rural vinculada a um produtor e cidade.",
        request=PropriedadeSerializer,
        responses={201: PropriedadeSerializer}
    ),
    retrieve=extend_schema(
        summary="Detalhar propriedade",
        description="Retorna os dados de uma propriedade pelo seu ID.",
        responses={200: PropriedadeSerializer}
    ),
    update=extend_schema(
        summary="Atualizar propriedade",
        description="Atualiza os dados de uma propriedade existente.",
        request=PropriedadeSerializer,
        responses={200: PropriedadeSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de propriedade",
        description="Atualiza parcialmente os dados de uma propriedade. Apenas os campos enviados serão alterados.",
        request=PropriedadeSerializer,
        responses={200: PropriedadeSerializer}
    ),
    destroy=extend_schema(
        summary="Deletar propriedade",
        description="Remove uma propriedade do sistema.",
        responses={204: None}
    ),
)
class PropriedadeViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de Propriedade.
    """
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer
    lookup_field = 'id_propriedade'


@extend_schema_view(
    list=extend_schema(
        summary="Listar culturas",
        description="Retorna todas as culturas agrícolas cadastradas.",
        responses={200: CulturaSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar cultura",
        description="Cria uma nova cultura agrícola vinculada a uma propriedade e tipo de cultura.",
        request=CulturaSerializer,
        responses={201: CulturaSerializer}
    ),
    retrieve=extend_schema(
        summary="Detalhar cultura",
        description="Retorna os dados de uma cultura pelo seu ID.",
        responses={200: CulturaSerializer}
    ),
    update=extend_schema(
        summary="Atualizar cultura",
        description="Atualiza os dados de uma cultura existente.",
        request=CulturaSerializer,
        responses={200: CulturaSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de cultura",
        description="Atualiza parcialmente os dados de uma cultura. Apenas os campos enviados serão alterados.",
        request=CulturaSerializer,
        responses={200: CulturaSerializer}
    ),
    destroy=extend_schema(
        summary="Deletar cultura",
        description="Remove uma cultura do sistema.",
        responses={204: None}
    ),
)
class CulturaViewSet(LoggingModelViewSet):
    """
    ViewSet para operações CRUD de Cultura.
    """
    queryset = Cultura.objects.all()
    serializer_class = CulturaSerializer
    lookup_field = 'id_cultura'


@extend_schema(
    summary="Dashboard consolidado",
    description=(
        "Retorna estatísticas agregadas do sistema, incluindo total de fazendas, hectares, "
        "culturas plantadas, distribuição de fazendas por estado e uso do solo."
    ),
    responses={
        200: OpenApiExample(
            'Exemplo de resposta',
            value={
                "total_fazendas": 10,
                "total_hectares": 1500,
                "fazendas_por_estado": [
                    {"nome_estado": "SP", "qtd_fazendas": 5, "total_hectares": 800}
                ],
                "culturas_plantadas": [
                    {"tipo_cultura": "Grãos", "qtd": 7}
                ],
                "uso_do_solo": {
                    "total_agricultavel": 1200,
                    "total_vegetacao": 300
                }
            },
            response_only=True
        )
    }
)
class DashboardView(APIView):
    """
    Endpoint somente leitura para estatísticas consolidadas do sistema.
    """
    def get(self, request):
        logger.info("Dashboard acessado por %s", request.user)
        start = time.monotonic()
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
            raise
        finally:
            elapsed = time.monotonic() - start
            logger.info("Tempo de execução do dashboard: %.3fs", elapsed)

