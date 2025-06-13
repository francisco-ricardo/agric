#!/bin/bash
# Este script envia uma requisição DELETE para remover uma cultura específica pelo ID.

curl -v -X DELETE http://localhost:8000/api/culturas/1/
