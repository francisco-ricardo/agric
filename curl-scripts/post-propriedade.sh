#!/bin/bash

curl -v -X POST http://localhost:8000/api/propriedades/ \
  -H "Content-Type: application/json" \
  -d '{"nome_propriedade": "Fazenda Boa Vista", "area_total": 100.0, "area_agricultavel": 60.0, "area_vegetacao": 40.0, "cidade": 1, "produtor": "12345678909"}'
