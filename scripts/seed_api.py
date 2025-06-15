#!/usr/bin/env python3
"""
Script de seed para popular a base de dados da API agric.

Este script utiliza a API REST para criar:
- Estados e cidades brasileiras válidas
- Tipos de cultura agrícolas reais
- Produtores rurais com dados fictícios
- Propriedades com áreas variadas e consistentes
- Culturas variadas por propriedade e safra, respeitando regras de unicidade e área

Características:
- Gera dados variados usando listas fixas e Faker
- Garante unicidade e integridade referencial conforme regras de negócio
- Pode ser executado múltiplas vezes após limpar a base

Uso:
    python scripts/seed_api.py

"""
import requests
import random
from datetime import datetime
from faker import Faker


def main():
    """
    Função principal que executa o processo de seed.
    """

    fake = Faker('pt_BR')

    
    # Estados
    estados_brasileiros = (
        "Bahia", "Ceará", "Goiás", "Mato Grosso", "Minas Gerais", 
        "Paraná", "Rio Grande do Sul", "Santa Catarina",
        "São Paulo", "Tocantins",
    )
    estados = []
    for i in range(10):
        nome_estado = estados_brasileiros[i]
        estado = post("estados", {"nome_estado": nome_estado})
        if estado:
            estados.append(estado)

    
    # Cidades
    cidades_brasil = (
        "Salvador", "Fortaleza", "Goiânia", "Cuiabá", "Belo Horizonte",
        "Guarapuava", "Porto Alegre", "Chapecó", "Ribeirão Preto", "Palmas",
    )
    cidades = []
    for i in range(10):
        nome_cidade = cidades_brasil[i]
        estado_id = estados[i]["id_estado"]
        cidades.append(post("cidades", {"nome_cidade": nome_cidade, "estado": estado_id}))

    
    # Tipos de Cultura
    tipos_cultura_validos = ("Soja", "Milho", "Café", "Arroz", "Trigo",)
    tipos_cultura = []
    for i in range(5):
        nome = tipos_cultura_validos[i]
        tipo_cultura = post("tipos-cultura", {"tipo_cultura": nome})
        if tipo_cultura:
            tipos_cultura.append(tipo_cultura)

    
    # Produtores
    produtores = []
    for i in range(10):
        nome = fake.unique.name()
        cpf = fake.unique.cpf()
        cidade_id = cidades[i]["id_cidade"]
        produtores.append(post("produtores", {
            "nome_produtor": nome,
            "cpf_cnpj": cpf,
            "cidade": cidade_id
        }))


    # Propriedades
    propriedades = []
    for idx, produtor in enumerate(produtores):
        for j in range(1, (idx % 3) + 2):
            nome = fake.unique.company()
            area_total = round(random.uniform(50, 500), 2)
            area_agricultavel = round(random.uniform(area_total * 0.1, area_total * 0.9), 2)
            max_vegetacao = area_total - area_agricultavel
            area_vegetacao = round(random.uniform(0, max_vegetacao), 2)
            prop = post("propriedades", {
                "nome_propriedade": nome,
                "produtor": produtor["cpf_cnpj"],
                "cidade": cidades[idx % 10]["id_cidade"],
                "area_total": area_total,
                "area_agricultavel": area_agricultavel,
                "area_vegetacao": area_vegetacao
            })
            if prop:
                propriedades.append(prop)

    
    # Culturas
    anos_safra = (datetime.now().year - 1, datetime.now().year,)

    for prop in propriedades:
        num_culturas = random.randint(1, 4)  # de 1 a 4 culturas por propriedade
        combinacoes = []
        for ano in anos_safra:
            for tipo in tipos_cultura:
                combinacoes.append((ano, tipo))
        random.shuffle(combinacoes)
        area_disponivel = prop["area_agricultavel"]
        for i in range(num_culturas):
            if not combinacoes or area_disponivel < 5:
                break
            ano_safra, tipo_cultura = combinacoes.pop()
            # Sorteia uma área entre 5 e o máximo possível restante
            max_area = min(area_disponivel, 50)
            area_cultura = round(random.uniform(5, max_area), 2)
            area_disponivel -= area_cultura
            post("culturas", {
                "nome_cultura": tipo_cultura["tipo_cultura"],
                "propriedade": prop["id_propriedade"],
                "tipo_cultura": tipo_cultura["id_tipo_cultura"],
                "area": area_cultura,
                "ano_safra": ano_safra
            })

    print("Seed via API concluido!")


def post(endpoint, data) -> dict:
    """
    Envia uma requisição POST para a API para criar um novo recurso.
        :param endpoint: O endpoint da API onde o recurso será criado.
        :param data: Os dados a serem enviados no corpo da requisição.
        :return: O JSON retornado pela API ou None em caso de erro.
    """
    API_URL = "http://localhost:8000/api"
    r = requests.post(f"{API_URL}/{endpoint}/", json=data)
    if r.status_code not in (200, 201):
        print(f"Erro ao criar em {endpoint}: {r.status_code} - {r.text}")
    return r.json() if r.ok else None


if __name__ == "__main__":
    main()
    
    