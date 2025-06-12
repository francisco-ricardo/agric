from rest_framework import viewsets
from .models import Produtor
from .serializers import ProdutorSerializer

class ProdutorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Produtor.
    Permite listar, criar, atualizar e deletar produtores rurais.
    """
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer
    lookup_field = 'cpf_cnpj'
