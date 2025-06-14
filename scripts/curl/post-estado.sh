#!/bin/bash

curl -i -X POST http://localhost:8000/api/estados/ \
  -H "Content-Type: application/json" \
  -d '{"nome_estado": "Minas Gerais"}'
