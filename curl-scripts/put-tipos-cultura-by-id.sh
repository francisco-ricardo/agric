#!/bin/bash

curl -i -X PUT http://localhost:8000/api/tipos-cultura/1/ \
  -H "Content-Type: application/json" \
  -d '{"tipo_cultura": "Milho"}'

