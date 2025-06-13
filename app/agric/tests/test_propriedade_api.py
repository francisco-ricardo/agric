import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from agric.models import Cidade, Estado, Produtor

@pytest.mark.django_db
class TestPropriedadeAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('propriedade-list')
        self.estado = Estado.objects.create(nome_estado="Minas Gerais")
        self.cidade = Cidade.objects.create(nome_cidade="Uberlândia", estado=self.estado)
        self.produtor = Produtor.objects.create(cpf_cnpj="12345678909", tipo_documento="CPF", nome_produtor="Produtor Teste")

    def test_create_propriedade(self):
        data = {
            "nome_propriedade": "Fazenda Boa Vista",
            "area_total": 100.0,
            "area_agricultavel": 60.0,
            "area_vegetacao": 40.0,
            "cidade": self.cidade.id_cidade,
            "produtor": self.produtor.cpf_cnpj
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["nome_propriedade"] == "Fazenda Boa Vista"

    def test_area_invalida(self):
        data = {
            "nome_propriedade": "Fazenda Inválida",
            "area_total": 100.0,
            "area_agricultavel": 80.0,
            "area_vegetacao": 30.0,
            "cidade": self.cidade.id_cidade,
            "produtor": self.produtor.cpf_cnpj
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 400

        