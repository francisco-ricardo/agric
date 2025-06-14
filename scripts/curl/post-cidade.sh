#!/bin/bash

curl -i -X POST http://localhost:8000/api/cidades/ \
  -H "Content-Type: application/json" \
  -d '{"nome_cidade": "Uberlândia", "estado": 1}'
