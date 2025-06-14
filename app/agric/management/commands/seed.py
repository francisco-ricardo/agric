"""
Comando Django para popular o banco de dados com dados realistas para testes e desenvolvimento.

- Cria estados e cidades brasileiras válidas (listas fixas)
- Cria tipos de cultura agrícolas reais (lista fixa)
- Gera produtores com dados fictícios únicos
- Gera propriedades com áreas variadas e consistentes
- Gera culturas variadas por propriedade e safra, respeitando unicidade

Uso:
    python manage.py seed
"""

from django.core.management.base import BaseCommand
from agric.models import Estado, Cidade, TipoCultura, Produtor, Propriedade, Cultura
from agric.validators import get_document_type
from faker import Faker
import random
from datetime import datetime

class Command(BaseCommand):
    help = "Popula o banco de dados com dados realistas para testes e desenvolvimento."

    def handle(self, *args, **kwargs):
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

        # Tipos de cultura
        tipos_cultura_nomes = [
            "Soja", "Milho", "Cana-de-açúcar", "Café", "Algodão",
            "Arroz", "Feijão", "Trigo", "Laranja", "Banana"
        ]
        tipos_cultura = [TipoCultura.objects.get_or_create(tipo_cultura=nome)[0] for nome in tipos_cultura_nomes]

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

        self.stdout.write(self.style.SUCCESS("Seed via ORM concluído!"))
        