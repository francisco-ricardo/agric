import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
class TestProdutorAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('produtor-list')

    def test_create_produtor_cpf_valido(self):
        """Requisito 1, 2: Cadastro e validação de CPF"""
        data = {"cpf_cnpj": "12345678909", "nome_produtor": "Produtor CPF"}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["tipo_documento"] == "CPF"

    def test_create_produtor_cnpj_valido(self):
        """Requisito 1, 2: Cadastro e validação de CNPJ"""
        data = {"cpf_cnpj": "11222333000181", "nome_produtor": "Produtor CNPJ"}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data["tipo_documento"] == "CNPJ"

    def test_create_produtor_documento_invalido(self):
        """Requisito 2: Validação de documento inválido"""
        data = {"cpf_cnpj": "123", "nome_produtor": "Inválido"}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 400
        assert "cpf_cnpj" in response.data

    def test_update_produtor(self):
        """Requisito 1: Edição de produtor"""
        data = {"cpf_cnpj": "12345678909", "nome_produtor": "Produtor"}
        self.client.post(self.url, data, format='json')
        update_url = f"{self.url}12345678909/"
        response = self.client.patch(update_url, {"nome_produtor": "Novo Nome"}, format='json')
        assert response.status_code == 200
        assert response.data["nome_produtor"] == "Novo Nome"

    def test_delete_produtor(self):
        """Requisito 1: Exclusão de produtor"""
        data = {"cpf_cnpj": "12345678909", "nome_produtor": "Produtor"}
        self.client.post(self.url, data, format='json')
        delete_url = f"{self.url}12345678909/"
        response = self.client.delete(delete_url)
        assert response.status_code == 204

    def test_list_produtores(self):
        """Requisito 1: Listagem de produtores"""
        self.client.post(self.url, {"cpf_cnpj": "12345678909", "nome_produtor": "Produtor"}, format='json')
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert any(p["cpf_cnpj"] == "12345678909" for p in response.data)
        