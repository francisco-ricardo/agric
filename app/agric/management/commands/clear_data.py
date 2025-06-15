"""
clear_data.py

Comando customizado do Django para limpar os dados das principais tabelas do app Agric.

Este comando remove todos os registros das tabelas relacionadas a produtores, propriedades, 
culturas, cidades, estados e tipos de cultura.
Útil para resetar o banco de dados durante o desenvolvimento ou para rodar cenários de 
testes limpos.

Uso:
    python manage.py clear_data
"""
from django.core.management.base import BaseCommand
from agric.models import Estado, Cidade, TipoCultura, Produtor, Propriedade, Cultura

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Comando Django para remover todos os dados das tabelas principais do app Agric.

    Remove registros de: Cultura, Propriedade, Produtor, Cidade, Estado, TipoCultura.
    """
    
    help = "Remove todos os dados das tabelas principais do app agric"

    def handle(self, *args, **kwargs):
        logger.info("Iniciando comando clear_data")
        Cultura.objects.all().delete()
        logger.info("Culturas removidas com sucesso!")
        Propriedade.objects.all().delete()
        logger.info("Propriedades removidas com sucesso!")
        Produtor.objects.all().delete()
        logger.info("Produtores removidos com sucesso!")
        TipoCultura.objects.all().delete()
        logger.info("Tipos de cultura removidos com sucesso!")
        Cidade.objects.all().delete()
        logger.info("Cidades removidas com sucesso!")
        Estado.objects.all().delete()
        logger.info("Estados removidos com sucesso!")
        logger.info("Dados removidos com sucesso!")
