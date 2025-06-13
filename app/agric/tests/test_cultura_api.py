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

    def test_create_cultura(self):
        data = {
            "ano_safra": 2025,
            "tipo_cultura": self.tipocultura.id_tipo_cultura,
            "propriedade": self.propriedade.id_propriedade
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["ano_safra"] == 2025

    def test_list_culturas(self):
        self.client.post(self.url, {
            "ano_safra": 2024,
            "tipo_cultura": self.tipocultura.id_tipo_cultura,
            "propriedade": self.propriedade.id_propriedade
        }, format='json')
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert any(c["ano_safra"] == 2024 for c in response.data)