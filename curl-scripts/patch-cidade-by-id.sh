#!/bin/bash

curl -i -X PATCH http://localhost:8000/api/cidades/1/ \
  -H "Content-Type: application/json" \
  -d '{"nome_cidade": "Uberaba"}'
