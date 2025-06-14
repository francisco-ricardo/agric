import pytest
from rest_framework.test import APIClient

def criar_estado(client, nome_estado):
    resp = client.post("/api/estados/", {"nome_estado": nome_estado}, format="json")
    assert resp.status_code == 201, f"Erro ao criar estado: {resp.data}"
    return resp.data.get("id_estado")

def criar_cidade(client, nome_cidade, estado_id):
    resp = client.post("/api/cidades/", {"nome_cidade": nome_cidade, "estado": estado_id}, format="json")
    assert resp.status_code == 201, f"Erro ao criar cidade: {resp.data}"
    return resp.data.get("id_cidade")

def criar_produtor(client, nome_produtor, cpf_cnpj, tipo_documento):
    resp = client.post("/api/produtores/", {
        "nome_produtor": nome_produtor,
        "cpf_cnpj": cpf_cnpj,
        "tipo_documento": tipo_documento
    }, format="json")
    assert resp.status_code == 201, f"Erro ao criar produtor: {resp.data}"
    return cpf_cnpj  # Use o CPF/CNPJ como identificador

def criar_propriedade(client, nome_propriedade, produtor_cpf_cnpj, cidade_id, area_total, area_agricultavel, area_vegetacao):
    resp = client.post("/api/propriedades/", {
        "nome_propriedade": nome_propriedade,
        "produtor": produtor_cpf_cnpj,
        "cidade": cidade_id,
        "area_total": area_total,
        "area_agricultavel": area_agricultavel,
        "area_vegetacao": area_vegetacao
    }, format="json")
    assert resp.status_code == 201, f"Erro ao criar propriedade: {resp.data}"
    return resp.data.get("id_propriedade")

def criar_tipocultura(client, tipo_cultura):
    resp = client.post("/api/tipos-cultura/", {"tipo_cultura": tipo_cultura}, format="json")
    assert resp.status_code == 201, f"Erro ao criar tipo de cultura: {resp.data}"
    return resp.data.get("id_tipo")

def criar_cultura(client, propriedade_id, tipocultura_id, nome_cultura, safra, area_plantada):
    resp = client.post("/api/culturas/", {
        "propriedade": propriedade_id,
        "tipo_cultura": tipocultura_id,
        "nome_cultura": nome_cultura,
        "safra": safra,
        "area_plantada": area_plantada
    }, format="json")
    return resp

@pytest.mark.django_db
def test_fluxo_integracao_sucesso():
    client = APIClient()
    estado_id = criar_estado(client, "Minas Gerais")
    cidade_id = criar_cidade(client, "Uberlândia", estado_id)
    produtor_cpf = criar_produtor(client, "João da Silva", "52998224725", "CPF")
    propriedade_id = criar_propriedade(
        client, "Fazenda Boa Vista", produtor_cpf, cidade_id, 100.0, 80.0, 20.0
    )
    tipocultura_id = criar_tipocultura(client, "Grãos")
    resp_cultura = criar_cultura(client, propriedade_id, tipocultura_id, "Soja", 2024, 80.0)
    assert resp_cultura.status_code == 201, f"Erro ao criar cultura: {resp_cultura.data}"
    cultura_id = resp_cultura.data.get("id_cultura")

    resp_dashboard = client.get("/api/dashboard/")
    assert resp_dashboard.status_code == 200
    assert resp_dashboard.data.get("total_estados", 0) >= 1
    assert resp_dashboard.data.get("total_cidades", 0) >= 1
    assert resp_dashboard.data.get("total_produtores", 0) >= 1
    assert resp_dashboard.data.get("total_propriedades", 0) >= 1
    assert resp_dashboard.data.get("total_culturas", 0) >= 1

@pytest.mark.django_db
def test_nao_permite_nome_estado_duplicado():
    client = APIClient()
    criar_estado(client, "Minas Gerais")
    resp2 = client.post("/api/estados/", {"nome_estado": "Minas Gerais"}, format="json")
    assert resp2.status_code == 400
    assert "nome_estado" in resp2.data

@pytest.mark.django_db
def test_nao_permite_cultura_duplicada_mesma_safra_propriedade():
    client = APIClient()
    estado_id = criar_estado(client, "São Paulo")
    cidade_id = criar_cidade(client, "Franca", estado_id)
    produtor_cpf = criar_produtor(client, "Maria Oliveira", "62648716050", "CPF")
    propriedade_id = criar_propriedade(
        client, "Sítio das Flores", produtor_cpf, cidade_id, 50.0, 30.0, 20.0
    )
    tipocultura_id = criar_tipocultura(client, "Frutas")
    cultura_payload = {
        "propriedade": propriedade_id,
        "tipo_cultura": tipocultura_id,
        "nome_cultura": "Laranja",
        "safra": 2025,
        "area_plantada": 20.0
    }
    resp1 = client.post("/api/culturas/", cultura_payload, format="json")
    assert resp1.status_code == 201
    resp2 = client.post("/api/culturas/", cultura_payload, format="json")
    assert resp2.status_code == 400
    assert "non_field_errors" in resp2.data

@pytest.mark.django_db
def test_nao_permite_area_plantada_maior_que_total():
    client = APIClient()
    estado_id = criar_estado(client, "Paraná")
    cidade_id = criar_cidade(client, "Londrina", estado_id)
    produtor_cpf = criar_produtor(client, "Carlos Souza", "11144477735", "CPF")
    propriedade_id = criar_propriedade(
        client, "Chácara Esperança", produtor_cpf, cidade_id, 30.0, 20.0, 10.0
    )
    tipocultura_id = criar_tipocultura(client, "Hortaliças")
    resp = criar_cultura(client, propriedade_id, tipocultura_id, "Alface", 2025, 40.0)
    assert resp.status_code == 400
    assert "area_plantada" in resp.data or "non_field_errors" in resp.data

@pytest.mark.django_db
def test_delecao_em_cascata_produtor():
    client = APIClient()
    estado_id = criar_estado(client, "Bahia")
    cidade_id = criar_cidade(client, "Barreiras", estado_id)
    produtor_cpf = criar_produtor(client, "Ana Lima", "39053344705", "CPF")
    propriedade_id = criar_propriedade(
        client, "Fazenda Barreiras", produtor_cpf, cidade_id, 60.0, 40.0, 20.0
    )
    tipocultura_id = criar_tipocultura(client, "Cereais")
    resp_cultura = criar_cultura(client, propriedade_id, tipocultura_id, "Milho", 2025, 30.0)
    assert resp_cultura.status_code == 201
    cultura_id = resp_cultura.data.get("id_cultura")

    resp_del = client.delete(f"/api/produtores/{produtor_cpf}/")
    assert resp_del.status_code == 204
    resp_prop = client.get(f"/api/propriedades/{propriedade_id}/")
    assert resp_prop.status_code == 404
    resp_cult = client.get(f"/api/culturas/{cultura_id}/")
    assert resp_cult.status_code == 404