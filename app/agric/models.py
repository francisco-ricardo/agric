"""
models.py

Modelos de dados do app Agric.

Este módulo define as entidades principais do sistema de gestão agrícola:
- Produtor: representa um produtor rural, identificado por CPF ou CNPJ.
- Estado: representa uma unidade federativa.
- Cidade: representa um município vinculado a um estado.
- TipoCultura: representa um tipo de cultura agrícola (ex: Grãos, Frutas).
- Propriedade: representa uma fazenda/propriedade rural, vinculada a um produtor e cidade.
- Cultura: representa o plantio de um tipo de cultura em uma propriedade em determinado ano-safra.

Cada model implementa validações de negócio e métodos utilitários para garantir a integridade dos dados.
"""
from django.db import models
from django.core.exceptions import ValidationError
from .validators import is_valid_cpf, is_valid_cnpj, get_document_type
import re

import logging
logger = logging.getLogger(__name__)


class Produtor(models.Model):
    """
    Representa um produtor rural, identificado por CPF ou CNPJ.
    Valida o documento e define o tipo automaticamente.
    """
    CPF = 'CPF'
    CNPJ = 'CNPJ'
    TIPO_DOCUMENTO_CHOICES = [
        (CPF, 'CPF'),
        (CNPJ, 'CNPJ'),
    ]

    cpf_cnpj = models.CharField(primary_key=True, max_length=20, unique=True)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES)
    nome_produtor = models.CharField(max_length=255)

    class Meta:
        db_table = "produtor"    

    def clean(self):
        # Remove máscara
        self.cpf_cnpj = re.sub(r'\D', '', self.cpf_cnpj)
        tipo = get_document_type(self.cpf_cnpj)
        if tipo == 'CPF':
            if not is_valid_cpf(self.cpf_cnpj):
                logger.warning("CPF inválido recebido: %s", self.cpf_cnpj)
                raise ValidationError({'cpf_cnpj': 'CPF inválido'})
        elif tipo == 'CNPJ':
            if not is_valid_cnpj(self.cpf_cnpj):
                logger.warning("CNPJ inválido recebido: %s", self.cpf_cnpj)
                raise ValidationError({'cpf_cnpj': 'CNPJ inválido'})
        else:
            logger.warning("Documento inválido recebido: %s", self.cpf_cnpj)
            raise ValidationError({'cpf_cnpj': 'Documento deve ser CPF ou CNPJ válido'})
        self.tipo_documento = tipo

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_produtor} ({self.cpf_cnpj})"


class Estado(models.Model):
    """
    Representa uma unidade federativa (estado).
    """
    id_estado = models.BigAutoField(primary_key=True)
    nome_estado = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "estado"

    def __str__(self):
        return self.nome_estado
    

class Cidade(models.Model):
    """
    Representa um município vinculado a um estado.
    Garante unicidade do nome da cidade por estado.
    """
    id_cidade = models.BigAutoField(primary_key=True)
    nome_cidade = models.CharField(max_length=255)
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE, related_name='cidades')

    class Meta:
        db_table = "cidade"
        unique_together = ('nome_cidade', 'estado')

    def __str__(self):
        return f"{self.nome_cidade} ({self.estado.nome_estado})"


class TipoCultura(models.Model):
    """
    Representa um tipo de cultura agrícola (ex: Grãos, Frutas).
    """
    id_tipo_cultura = models.BigAutoField(primary_key=True)
    tipo_cultura = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "tipo_cultura"

    def __str__(self):
        return self.tipo_cultura
    

class Propriedade(models.Model):
    """
    Representa uma fazenda/propriedade rural.
    Vinculada a um produtor e cidade.
    Valida que a soma das áreas agricultável e de vegetação não ultrapassa a área total.
    """
    id_propriedade = models.BigAutoField(primary_key=True)
    nome_propriedade = models.CharField(max_length=255)
    area_total = models.FloatField()
    area_agricultavel = models.FloatField()
    area_vegetacao = models.FloatField()
    cidade = models.ForeignKey('Cidade', on_delete=models.CASCADE, related_name='propriedades')
    produtor = models.ForeignKey('Produtor', on_delete=models.CASCADE, related_name='propriedades')

    class Meta:
        db_table = "propriedade"

    def clean(self):
        if self.area_agricultavel + self.area_vegetacao > self.area_total:
            logger.warning("Área inválida em Propriedade '%s': agric.=%s + veget.=%s > total=%s",
                self.nome_propriedade, self.area_agricultavel, self.area_vegetacao, self.area_total)
            raise ValidationError("A soma das áreas agricultável e de vegetação não pode ultrapassar a área total.")


    def __str__(self):
        return self.nome_propriedade


class Cultura(models.Model):
    """
    Representa o plantio de um tipo de cultura em uma propriedade em determinado ano-safra.
    Garante unicidade por (ano_safra, tipo_cultura, propriedade).
    """
    id_cultura = models.BigAutoField(primary_key=True)
    ano_safra = models.IntegerField()
    tipo_cultura = models.ForeignKey('TipoCultura', on_delete=models.CASCADE, related_name='culturas')
    propriedade = models.ForeignKey('Propriedade', on_delete=models.CASCADE, related_name='culturas')

    class Meta:
        db_table = "cultura"
        unique_together = ('ano_safra', 'tipo_cultura', 'propriedade')

    def __str__(self):
        return f"{self.tipo_cultura.tipo_cultura} - {self.ano_safra} ({self.propriedade.nome_propriedade})"
    