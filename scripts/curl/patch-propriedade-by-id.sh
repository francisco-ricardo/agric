#!/bin/bash
# Atualiza uma propriedade pelo ID

curl -v -X PATCH http://localhost:8000/api/propriedades/1/ \
  -H "Content-Type: application/json" \
  -d '{"nome_propriedade": "Fazenda Parcial"}'