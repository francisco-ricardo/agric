#!/bin/bash
# Este script envia uma requisição POST para criar uma nova cultura.

curl -v -X POST http://localhost:8000/api/culturas/ \
  -H "Content-Type: application/json" \
  -d '{"ano_safra": 2025, "tipo_cultura": 1, "propriedade": 1}'