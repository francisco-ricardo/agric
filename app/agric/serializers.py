"""
serializers.py

Serializers do app Agric para a API REST.

Este módulo define os serializers responsáveis por validar, serializar e desserializar
os dados das principais entidades do sistema agric:
- Produtor
- Estado
- Cidade
- TipoCultura
- Propriedade
- Cultura

Cada serializer garante as regras de negócio e integridade dos dados para a API.
"""
from rest_framework import serializers
from .models import Produtor
from .models import Estado
from .models import Cidade
from .models import TipoCultura
from .models import Propriedade
from .models import Cultura


class ProdutorSerializer(serializers.ModelSerializer):
    """
    Serializador para o model Produtor.
    - Valida CPF/CNPJ.
    - Preenche automaticamente o tipo de documento.
    - Usa o campo cpf_cnpj como identificador.
    """
    class Meta:
        model = Produtor
        fields = ['cpf_cnpj', 'tipo_documento', 'nome_produtor']
        read_only_fields = ['tipo_documento']

    
    def create(self, validated_data):
        """
        Cria um novo Produtor.
        Define automaticamente o tipo de documento (CPF ou CNPJ) com base no tamanho 
        do campo cpf_cnpj.
        """
        cpf_cnpj = validated_data.get("cpf_cnpj", "")
        if len(cpf_cnpj) == 11:
            validated_data["tipo_documento"] = "CPF"
        elif len(cpf_cnpj) == 14:
            validated_data["tipo_documento"] = "CNPJ"
        else:
            validated_data["tipo_documento"] = ""
        return super().create(validated_data)


    def validate_cpf_cnpj(self, value):
        """
        Valida o campo cpf_cnpj, garantindo que contenha apenas números e 
        tenha 11 (CPF) ou 14 (CNPJ) dígitos.
        """
        value = ''.join(filter(str.isdigit, value))
        if not (len(value) == 11 or len(value) == 14):
            raise serializers.ValidationError("CPF deve ter 11 dígitos ou CNPJ 14 dígitos.")
        return value
    

class EstadoSerializer(serializers.ModelSerializer):
    """
    Serializador para o model Estado.
    """
    class Meta:
        model = Estado
        fields = ['id_estado', 'nome_estado']


class CidadeSerializer(serializers.ModelSerializer):
    """
    Serializador para o model Cidade.
    - Serializa id, nome e estado associado.
    """
    class Meta:
        model = Cidade
        fields = ['id_cidade', 'nome_cidade', 'estado']


class TipoCulturaSerializer(serializers.ModelSerializer):
    """
    Serializador para o model TipoCultura.
    - Serializa id e nome do tipo de cultura.
    """
    class Meta:
        model = TipoCultura
        fields = ['id_tipo_cultura', 'tipo_cultura']


class PropriedadeSerializer(serializers.ModelSerializer):
    """
    Serializador para o model Propriedade.
    - Valida soma das áreas agricultável e de vegetação.
    - Serializa todos os campos principais da propriedade.
    """
    class Meta:
        model = Propriedade
        fields = [
            'id_propriedade', 'nome_propriedade', 'area_total',
            'area_agricultavel', 'area_vegetacao', 'cidade', 'produtor'
        ]

    def validate(self, data):
        """
        Valida se a soma das áreas agricultável e de vegetação não ultrapassa a 
        área total da propriedade.
        """
        area_total = data.get('area_total')
        area_agricultavel = data.get('area_agricultavel')
        area_vegetacao = data.get('area_vegetacao')
        if area_total is not None and area_agricultavel is not None and area_vegetacao is not None:
            if area_agricultavel + area_vegetacao > area_total:
                raise serializers.ValidationError(
                    "A soma das áreas agricultável e de vegetação não pode ultrapassar a área total."
                )
        return data


class CulturaSerializer(serializers.ModelSerializer):
    """
    Serializador para o model Cultura.
    - Serializa id, ano_safra, tipo_cultura e propriedade.
    - Garante unicidade por (ano_safra, tipo_cultura, propriedade).
    """
    class Meta:
        model = Cultura
        fields = ['id_cultura', 'ano_safra', 'tipo_cultura', 'propriedade']


class FazendaPorEstadoSerializer(serializers.Serializer):
    """
    Serializados para representar o agrupamento de fazendas por estado no dashboard.
    """
    nome_estado = serializers.CharField(help_text="Nome do estado")
    qtd_fazendas = serializers.IntegerField(help_text="Quantidade de fazendas no estado")
    total_hectares = serializers.FloatField(help_text="Soma dos hectares das fazendas no estado")


class CulturaPlantadaSerializer(serializers.Serializer):
    """
    Serializador para representar o agrupamento de culturas plantadas no dashboard.
    """
    tipo_cultura = serializers.CharField(help_text="Nome do tipo de cultura")
    qtd = serializers.IntegerField(help_text="Quantidade de culturas plantadas desse tipo")


class UsoDoSoloSerializer(serializers.Serializer):
    """
    Serializador para representar o uso do solo agregado no dashboard.
    """
    total_agricultavel = serializers.FloatField(help_text="Área total agricultável (hectares)")
    total_vegetacao = serializers.FloatField(help_text="Área total de vegetação (hectares)")
    

class DashboardResponseSerializer(serializers.Serializer):
    """
    Serializador para a resposta do endpoint de dashboard consolidado.
    """
    total_fazendas = serializers.IntegerField(help_text="Total de fazendas cadastradas")
    total_hectares = serializers.FloatField(help_text="Soma total de hectares cadastrados")
    fazendas_por_estado = FazendaPorEstadoSerializer(many=True, help_text="Distribuição de fazendas por estado")
    culturas_plantadas = CulturaPlantadaSerializer(many=True, help_text="Distribuição de culturas plantadas")
    uso_do_solo = UsoDoSoloSerializer(help_text="Áreas agregadas de uso do solo")