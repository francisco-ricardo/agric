import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from agric.models import Estado, Cidade, Produtor, Propriedade, TipoCultura, Cultura

@pytest.mark.django_db
class TestDashboardAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('dashboard')
        estado = Estado.objects.create(nome_estado="Minas Gerais")
        cidade = Cidade.objects.create(nome_cidade="Uberlândia", estado=estado)
        produtor = Produtor.objects.create(cpf_cnpj="12345678909", tipo_documento="CPF", nome_produtor="Produtor Teste")
        propriedade = Propriedade.objects.create(
            nome_propriedade="Fazenda Teste",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            cidade=cidade,
            produtor=produtor
        )
        tipocultura = TipoCultura.objects.create(tipo_cultura="Soja")
        Cultura.objects.create(
            ano_safra=2025,
            tipo_cultura=tipocultura,
            propriedade=propriedade
        )

    def test_dashboard_response(self):
        """Requisito 7: Dashboard geral"""
        response = self.client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert "total_fazendas" in data
        assert "total_hectares" in data
        assert "fazendas_por_estado" in data
        assert "culturas" in data or "culturas_plantadas" in data
        assert "uso_solo" in data or "uso_do_solo" in data

    def test_dashboard_total_fazendas(self):
        """Requisito 7: Total de fazendas"""
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.json()["total_fazendas"] >= 1

    def test_dashboard_total_hectares(self):
        """Requisito 7: Total de hectares"""
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.json()["total_hectares"] >= 100.0

