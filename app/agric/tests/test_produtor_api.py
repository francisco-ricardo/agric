import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
class TestProdutorAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('produtor-list')

    def test_create_produtor_cpf(self):
        data = {
            "cpf_cnpj": "12345678909",  # CPF válido para teste
            "nome_produtor": "Produtor Teste"
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["tipo_documento"] == "CPF"
        assert response.data["cpf_cnpj"] == "12345678909"

    def test_create_produtor_cnpj(self):
        data = {
            "cpf_cnpj": "11222333000181",  # CNPJ válido para teste
            "nome_produtor": "Empresa Teste"
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["tipo_documento"] == "CNPJ"
        assert response.data["cpf_cnpj"] == "11222333000181"

    def test_create_produtor_invalid(self):
        data = {
            "cpf_cnpj": "123",  # Inválido
            "nome_produtor": "Produtor Inválido"
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 400
        assert "cpf_cnpj" in response.data
