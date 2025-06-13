#!/bin/bash
# Este script atualiza uma propriedade existente com base no ID fornecido.

curl -v -X PUT http://localhost:8000/api/propriedades/1/ \
  -H "Content-Type: application/json" \
  -d '{"nome_propriedade": "Fazenda Atualizada", "area_total": 120.0, "area_agricultavel": 70.0, "area_vegetacao": 50.0, "cidade": 1, "produtor": "12345678909"}'
