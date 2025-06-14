import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from agric.models import Estado

@pytest.mark.django_db
class TestCidadeAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('cidade-list')
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

    def test_update_cidade(self):
        resp = self.client.post(self.url, {"nome_cidade": "Patos", "estado": self.estado.id_estado}, format='json')
        cidade_id = resp.data["id_cidade"]
        resp = self.client.patch(f"{self.url}{cidade_id}/", {"nome_cidade": "Patos de Minas"}, format='json')
        assert resp.status_code == 200
        assert resp.data["nome_cidade"] == "Patos de Minas"

    def test_delete_cidade(self):
        resp = self.client.post(self.url, {"nome_cidade": "Araxá", "estado": self.estado.id_estado}, format='json')
        cidade_id = resp.data["id_cidade"]
        resp = self.client.delete(f"{self.url}{cidade_id}/")
        assert resp.status_code == 204