import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
class TestTipoCulturaAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('tipocultura-list')

    def test_create_tipocultura(self):
        data = {"tipo_cultura": "Soja"}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["tipo_cultura"] == "Soja"

    def test_list_tiposcultura(self):
        self.client.post(self.url, {"tipo_cultura": "Milho"}, format='json')
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert any(tc["tipo_cultura"] == "Milho" for tc in response.data)

    def test_update_tipocultura(self):
        resp = self.client.post(self.url, {"tipo_cultura": "Café"}, format='json')
        tipo_id = resp.data["id_tipo_cultura"]
        resp = self.client.patch(f"{self.url}{tipo_id}/", {"tipo_cultura": "Café Arábica"}, format='json')
        assert resp.status_code == 200
        assert resp.data["tipo_cultura"] == "Café Arábica"

    def test_delete_tipocultura(self):
        resp = self.client.post(self.url, {"tipo_cultura": "Trigo"}, format='json')
        tipo_id = resp.data["id_tipo_cultura"]
        resp = self.client.delete(f"{self.url}{tipo_id}/")
        assert resp.status_code == 204