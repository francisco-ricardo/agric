"""
serializers.py

Serializers do app Agric para a API REST.

- ProdutorSerializer: Responsável por serializar e validar os dados do model Produtor.
    - Garante que o campo cpf_cnpj seja um CPF ou CNPJ válido (apenas números, 11 ou 14 dígitos).
    - O campo tipo_documento é preenchido automaticamente pelo model e é somente leitura na API.
    - Utiliza ModelSerializer para reaproveitar validações e facilitar manutenção.
"""
from rest_framework import serializers
from .models import Produtor
from .models import Estado
from .models import Cidade


class ProdutorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produtor
        fields = ['cpf_cnpj', 'tipo_documento', 'nome_produtor']
        read_only_fields = ['tipo_documento']

    
    def create(self, validated_data):
        cpf_cnpj = validated_data.get("cpf_cnpj", "")
        if len(cpf_cnpj) == 11:
            validated_data["tipo_documento"] = "CPF"
        elif len(cpf_cnpj) == 14:
            validated_data["tipo_documento"] = "CNPJ"
        else:
            validated_data["tipo_documento"] = ""
        return super().create(validated_data)


    def validate_cpf_cnpj(self, value):
        value = ''.join(filter(str.isdigit, value))
        if not (len(value) == 11 or len(value) == 14):
            raise serializers.ValidationError("CPF deve ter 11 dígitos ou CNPJ 14 dígitos.")
        return value
    

#


class EstadoSerializer(serializers.ModelSerializer):
    """
    Serializador para o model Estado.
    """
    class Meta:
        model = Estado
        fields = ['id_estado', 'nome_estado']


#

class CidadeSerializer(serializers.ModelSerializer):
    """
    Serializador para o model Cidade.
    """
    class Meta:
        model = Cidade
        fields = ['id_cidade', 'nome_cidade', 'estado']


    