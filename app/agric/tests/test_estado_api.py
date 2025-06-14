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

    def test_update_estado(self):
        resp = self.client.post(self.url, {"nome_estado": "Bahia"}, format='json')
        estado_id = resp.data["id_estado"]
        resp = self.client.patch(f"{self.url}{estado_id}/", {"nome_estado": "Bahia Atualizada"}, format='json')
        assert resp.status_code == 200
        assert resp.data["nome_estado"] == "Bahia Atualizada"

    def test_delete_estado(self):
        resp = self.client.post(self.url, {"nome_estado": "Paraná"}, format='json')
        estado_id = resp.data["id_estado"]
        resp = self.client.delete(f"{self.url}{estado_id}/")
        assert resp.status_code == 204