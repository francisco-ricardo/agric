from django.db import models
from django.core.exceptions import ValidationError
from .validators import is_valid_cpf, is_valid_cnpj, get_document_type
import re

class Produtor(models.Model):
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
                raise ValidationError({'cpf_cnpj': 'CPF inválido'})
        elif tipo == 'CNPJ':
            if not is_valid_cnpj(self.cpf_cnpj):
                raise ValidationError({'cpf_cnpj': 'CNPJ inválido'})
        else:
            raise ValidationError({'cpf_cnpj': 'Documento deve ser CPF ou CNPJ válido'})
        self.tipo_documento = tipo

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_produtor} ({self.cpf_cnpj})"

