#!/bin/bash
# Este script envia uma requisição PATCH para atualizar parcialmente uma cultura específica pelo ID.

curl -v -X PATCH http://localhost:8000/api/culturas/1/ \
  -H "Content-Type: application/json" \
  -d '{"ano_safra": 2027}'