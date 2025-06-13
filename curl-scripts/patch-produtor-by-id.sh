#!/bin/bash

curl -v -X PATCH http://localhost:8000/api/produtores/12345678909/ \
  -H "Content-Type: application/json" \
  -d '{"nome_produtor": "Nome Parcialmente Atualizado"}'
