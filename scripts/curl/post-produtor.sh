#!/bin/sh

curl -v -X POST http://localhost:8000/api/produtores/ \
  -H "Content-Type: application/json" \
  -d '{"cpf_cnpj": "12345678909", "nome_produtor": "Pedro da Silva"}'

