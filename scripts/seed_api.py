#!/usr/bin/env python3

import requests
import random
from datetime import datetime
from faker import Faker


def post(endpoint, data) -> dict:
    API_URL = "http://localhost:8000/api"
    r = requests.post(f"{API_URL}/{endpoint}/", json=data)
    if r.status_code not in (200, 201):
        print(f"Erro ao criar em {endpoint}: {r.status_code} - {r.text}")
    return r.json() if r.ok else None


if __name__ == "__main__":
    
    fake = Faker('pt_BR')

    # Estados
    estados_brasileiros = [
        "Bahia", "Ceará", "Goiás", "Mato Grosso", "Minas Gerais", 
        "Paraná", "Rio Grande do Sul", "Santa Catarina",
        "São Paulo", "Tocantins"
    ]
    estados = []
    for i in range(10):
        nome_estado = estados_brasileiros[i]
        estado = post("estados", {"nome_estado": nome_estado})
        if estado:
            estados.append(estado)

    # Cidades
    cidades_brasil = [
        "Salvador", "Fortaleza", "Goiânia", "Cuiabá", "Belo Horizonte",
        "Curitiba", "Porto Alegre", "Chapecó", "São Paulo", "Palmas"
    ]
    cidades = []
    for i in range(10):
        nome_cidade = cidades_brasil[i]
        estado_id = estados[i]["id_estado"]
        cidades.append(post("cidades", {"nome_cidade": nome_cidade, "estado": estado_id}))

    # Tipos de Cultura
    tipos_cultura = []
    for _ in range(5):
        nome = fake.unique.word().capitalize()
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

    # Culturas (5 exemplos)
    for i in range(5):
        nome = fake.unique.word().capitalize()
        area_cultura = round(random.uniform(5, propriedades[i]["area_agricultavel"]), 2)
        ano_safra = datetime.now().year
        cultura = post("culturas", {
            "nome_cultura": nome,
            "propriedade": propriedades[i]["id_propriedade"],
            "tipo_cultura": tipos_cultura[i]["id_tipo_cultura"],
            "area": area_cultura,
            "ano_safra": ano_safra
        })





    # propriedades = []
    # for idx, produtor in enumerate(produtores):
    #     for j in range(1, (idx % 3) + 2):
    #         nome = fake.unique.company()
    #         cidade_id = cidades[idx % 10]["id_cidade"]
    #         prop = post("propriedades", {
    #             "nome_propriedade": nome,
    #             "produtor": produtor["cpf_cnpj"],
    #             "cidade": cidade_id,
    #             "area_total": 100.0,
    #             "area_agricultavel": 60.0,
    #             "area_vegetacao": 40.0
    #         })
    #         if prop:
    #             propriedades.append(prop)

    # # Culturas
    # for i in range(5):
    #     nome = fake.unique.word().capitalize()
    #     ano_safra = datetime.now().year  # ou outro valor desejado
    #     cultura = post("culturas", {
    #         "nome_cultura": nome,
    #         "propriedade": propriedades[i]["id_propriedade"],
    #         "tipo_cultura": tipos_cultura[i]["id_tipo_cultura"],
    #         "area": 20.0,
    #         "ano_safra": ano_safra
    # })

    print("Seed via API concluido!")