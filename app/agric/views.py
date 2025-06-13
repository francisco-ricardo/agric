from rest_framework import viewsets
from .models import Produtor
from .serializers import ProdutorSerializer

from .models import Estado
from .serializers import EstadoSerializer

from .models import Cidade
from .serializers import CidadeSerializer

from .models import TipoCultura
from .serializers import TipoCulturaSerializer


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