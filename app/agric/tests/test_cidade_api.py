import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from agric.models import Estado

@pytest.mark.django_db
class TestCidadeAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('cidade-list')
        # Cria um estado para usar nos testes
        self.estado = Estado.objects.create(nome_estado="Minas Gerais")

    def test_create_cidade(self):
        data = {"nome_cidade": "Uberlândia", "estado": self.estado.id_estado}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["nome_cidade"] == "Uberlândia"

    def test_list_cidades(self):
        self.client.post(self.url, {"nome_cidade": "Uberaba", "estado": self.estado.id_estado}, format='json')
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert any(c["nome_cidade"] == "Uberaba" for c in response.data)
