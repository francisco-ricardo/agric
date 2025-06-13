import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
class TestEstadoAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('estado-list')

    def test_create_estado(self):
        data = {"nome_estado": "Minas Gerais"}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["nome_estado"] == "Minas Gerais"

    def test_list_estados(self):
        self.client.post(self.url, {"nome_estado": "São Paulo"}, format='json')
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert any(e["nome_estado"] == "São Paulo" for e in response.data)