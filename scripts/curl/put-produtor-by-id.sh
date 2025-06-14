#!/bin/bash

curl -v -X PUT http://localhost:8000/api/produtores/12345678909/ \
  -H "Content-Type: application/json" \
  -d '{"cpf_cnpj": "12345678909", "nome_produtor": "Nome Atualizado"}'
