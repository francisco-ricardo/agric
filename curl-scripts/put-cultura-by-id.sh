#!/bin/bash
# Este script envia uma requisição PUT para atualizar uma cultura específica pelo ID.

curl -v -X PUT http://localhost:8000/api/culturas/1/ \
  -H "Content-Type: application/json" \
  -d '{"ano_safra": 2026, "tipo_cultura": 1, "propriedade": 1}'