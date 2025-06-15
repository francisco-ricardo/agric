"""
seed.py

Comando customizado do Django para popular o banco de dados do app Agric com dados de exemplo.

Este comando cria registros fictícios para produtores, propriedades, culturas, cidades, 
estados e tipos de cultura, facilitando o desenvolvimento, testes e demonstrações do sistema.

Uso:
    python manage.py seed
"""
from django.core.management.base import BaseCommand
from agric.models import Estado, Cidade, TipoCultura, Produtor, Propriedade, Cultura
from agric.validators import get_document_type
from faker import Faker
import random
from datetime import datetime

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Comando Django para inserir dados de exemplo nas tabelas principais do app Agric.

    Cria registros de: Estado, Cidade, TipoCultura, Produtor, Propriedade e Cultura.
    Útil para inicializar o sistema com dados mínimos para testes e desenvolvimento.
    """

    help = "Popula o banco de dados com dados realistas para testes e desenvolvimento."

    def handle(self, *args, **kwargs):

        logger.info("Iniciando comando seed para popular o banco de dados com dados de exemplo.")

        fake = Faker('pt_BR')
        Faker.seed(0)
        random.seed(0)

        # Estados e cidades
        estados_brasil = [
            {"nome_estado": "Acre", "cidades": ["Rio Branco", "Cruzeiro do Sul"]},
            {"nome_estado": "Bahia", "cidades": ["Salvador", "Feira de Santana"]},
            {"nome_estado": "Ceará", "cidades": ["Fortaleza", "Juazeiro do Norte"]},
            {"nome_estado": "Minas Gerais", "cidades": ["Belo Horizonte", "Uberlândia"]},
            {"nome_estado": "Paraná", "cidades": ["Curitiba", "Londrina"]},
            {"nome_estado": "Pernambuco", "cidades": ["Recife", "Caruaru"]},
            {"nome_estado": "Rio de Janeiro", "cidades": ["Rio de Janeiro", "Niterói"]},
            {"nome_estado": "Rio Grande do Sul", "cidades": ["Porto Alegre", "Caxias do Sul"]},
            {"nome_estado": "São Paulo", "cidades": ["São Paulo", "Campinas"]},
            {"nome_estado": "Tocantins", "cidades": ["Palmas", "Araguaína"]},
        ]
        cidades = []
        for est in estados_brasil:
            estado, _ = Estado.objects.get_or_create(nome_estado=est["nome_estado"])
            for nome_cidade in est["cidades"]:
                cidade, _ = Cidade.objects.get_or_create(nome_cidade=nome_cidade, estado=estado)
                cidades.append(cidade)
        logger.info(f"{len(cidades)} cidades criadas com sucesso!")
        logger.info(f"{len(estados_brasil)} estados criados com sucesso!")

        # Tipos de cultura
        tipos_cultura_nomes = [
            "Soja", "Milho", "Cana-de-açúcar", "Café", "Algodão",
            "Arroz", "Feijão", "Trigo", "Laranja", "Banana"
        ]
        tipos_cultura = [TipoCultura.objects.get_or_create(tipo_cultura=nome)[0] for nome in tipos_cultura_nomes]
        logger.info(f"{len(tipos_cultura)} tipos de cultura criados com sucesso!")

        # Produtores
        produtores = []
        for _ in range(20):
            for _ in range(10):  # tenta até conseguir um CPF único
                nome = fake.unique.name()
                cpf = fake.unique.cpf()
                tipo_documento = get_document_type(cpf)
                try:
                    produtor, created = Produtor.objects.get_or_create(
                        cpf_cnpj=cpf,
                        defaults={
                            "nome_produtor": nome,
                            "tipo_documento": tipo_documento
                        }
                    )
                    if created:
                        produtores.append(produtor)
                        break
                except Exception:
                    continue
        logger.info(f"{len(produtores)} produtores criados com sucesso!")
        if not produtores:
            logger.warning("Nenhum produtor foi criado. Verifique os dados gerados.")

        # Propriedades
        propriedades = []
        for produtor in produtores:
            for _ in range(random.randint(1, 3)):
                nome = fake.unique.company()
                cidade = random.choice(cidades)
                area_total = round(random.uniform(50, 500), 2)
                area_agricultavel = round(random.uniform(area_total * 0.3, area_total * 0.9), 2)
                area_vegetacao = round(area_total - area_agricultavel, 2)
                prop, _ = Propriedade.objects.get_or_create(
                    nome_propriedade=nome,
                    produtor=produtor,
                    cidade=cidade,
                    defaults={
                        "area_total": area_total,
                        "area_agricultavel": area_agricultavel,
                        "area_vegetacao": area_vegetacao
                    }
                )
                propriedades.append(prop)
        logger.info(f"{len(propriedades)} propriedades criadas com sucesso!")

        # Culturas
        anos_safra = [datetime.now().year - 1, datetime.now().year]
        for prop in propriedades:
            total_culturas = random.randint(1, 4)
            combinacoes = [(ano, tipo) for ano in anos_safra for tipo in tipos_cultura]
            random.shuffle(combinacoes)
            for _ in range(total_culturas):
                if not combinacoes:
                    break
                ano_safra, tipo_cultura = combinacoes.pop()
                Cultura.objects.get_or_create(
                    propriedade=prop,
                    tipo_cultura=tipo_cultura,
                    ano_safra=ano_safra
                )
        logger.info(f"{len(Cultura.objects.all())} culturas criadas com sucesso!")

        logger.info("Seed via ORM concluído com sucesso!")
        