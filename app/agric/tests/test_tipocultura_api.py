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