#!/bin/bash

curl -i -X POST http://localhost:8000/api/tipos-cultura/ \
  -H "Content-Type: application/json" \
  -d '{"tipo_cultura": "Soja"}'