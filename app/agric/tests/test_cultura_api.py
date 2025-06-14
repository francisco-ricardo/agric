import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from agric.models import Propriedade, TipoCultura, Cidade, Estado, Produtor

@pytest.mark.django_db
class TestCulturaAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('cultura-list')
        self.estado = Estado.objects.create(nome_estado="Minas Gerais")
        self.cidade = Cidade.objects.create(nome_cidade="Uberlândia", estado=self.estado)
        self.produtor = Produtor.objects.create(cpf_cnpj="12345678909", tipo_documento="CPF", nome_produtor="Produtor Teste")
        self.propriedade = Propriedade.objects.create(
            nome_propriedade="Fazenda Boa Vista",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            cidade=self.cidade,
            produtor=self.produtor
        )
        self.tipocultura = TipoCultura.objects.create(tipo_cultura="Soja")

    def test_create_varias_culturas_por_propriedade(self):
        """Requisito 4, 6: Várias culturas por propriedade/safra"""
        for ano in [2024, 2025]:
            for nome in ["Soja", "Milho"]:
                tipo = TipoCultura.objects.get_or_create(tipo_cultura=nome)[0]
                data = {
                    "ano_safra": ano,
                    "tipo_cultura": tipo.id_tipo_cultura,
                    "propriedade": self.propriedade.id_propriedade
                }
                response = self.client.post(self.url, data, format='json')
                assert response.status_code == 201

    def test_propriedade_sem_culturas(self):
        """Requisito 6: Propriedade sem culturas"""
        nova_propriedade = Propriedade.objects.create(
            nome_propriedade="Sem Cultura",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            cidade=self.cidade,
            produtor=self.produtor
        )
        response = self.client.get(self.url, {"propriedade": nova_propriedade.id_propriedade})
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_regra_unicidade_cultura_por_safra(self):
        """Requisito 6: Não permitir cultura duplicada na mesma safra/propriedade"""
        data = {
            "ano_safra": 2025,
            "tipo_cultura": self.tipocultura.id_tipo_cultura,
            "propriedade": self.propriedade.id_propriedade
        }
        self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 400
        