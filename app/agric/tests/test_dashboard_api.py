import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from agric.models import Estado, Cidade, Produtor, Propriedade, TipoCultura, Cultura

@pytest.mark.django_db
class TestDashboardAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('dashboard')
        # Cria dados mínimos para o dashboard
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
        response = self.client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        # Testa campos principais
        assert "total_fazendas" in data
        assert "total_hectares" in data
        assert "fazendas_por_estado" in data
        assert "culturas_plantadas" in data
        assert "uso_do_solo" in data
        # Testa valores principais
        assert data["total_fazendas"] == 1
        assert data["total_hectares"] == 100.0
        assert data["uso_do_solo"]["total_agricultavel"] == 60.0
        assert data["uso_do_solo"]["total_vegetacao"] == 40.0

    def test_dashboard_fazendas_por_estado(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        estados = data["fazendas_por_estado"]
        assert isinstance(estados, list)
        assert len(estados) > 0
        for estado in estados:
            assert "nome_estado" in estado
            assert "qtd_fazendas" in estado
            assert "total_hectares" in estado
            if estado["nome_estado"] == "Minas Gerais":
                assert estado["qtd_fazendas"] == 1
                assert estado["total_hectares"] == 100.0
