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
    ViewSet para CRUD de Produtor.
    Permite listar, criar, atualizar e deletar produtores rurais.
    """
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer
    lookup_field = 'cpf_cnpj'


#


class EstadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Estado.
    """
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    lookup_field = 'id_estado'


#

class CidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Cidade.
    """
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    lookup_field = 'id_cidade'


#


class TipoCulturaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de TipoCultura.
    """
    queryset = TipoCultura.objects.all()
    serializer_class = TipoCulturaSerializer
    lookup_field = 'id_tipo_cultura'


#


class PropriedadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Propriedade.
    """
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer
    lookup_field = 'id_propriedade'


#


class CulturaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Cultura.
    """
    queryset = Cultura.objects.all()
    serializer_class = CulturaSerializer
    lookup_field = 'id_cultura'


#


class DashboardView(APIView):
    """
    Endpoint para estatísticas do dashboard.
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
    