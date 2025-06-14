#!/bin/bash

curl -i -X PATCH http://localhost:8000/api/estados/1/ \
  -H "Content-Type: application/json" \
  -d '{"nome_estado": "Bahia"}'

