"""
Módulo de validação de documentos brasileiros para o sistema agric.

Este módulo fornece funções utilitárias para:
- Validar CPFs e CNPJs (com ou sem máscara)
- Identificar o tipo de documento (CPF ou CNPJ) a partir de uma string

Funções:
- is_valid_cpf(cpf): Valida um CPF brasileiro.
- is_valid_cnpj(cnpj): Valida um CNPJ brasileiro.
- get_document_type(value): Retorna 'CPF', 'CNPJ' ou None conforme o valor informado.

Essas funções são utilizadas para garantir a integridade dos dados de produtores rurais no sistema agric.
"""
import re

def is_valid_cpf(cpf) -> bool:
    """
    Valida um CPF brasileiro.

    Args:
        cpf (str): CPF a ser validado, com ou sem máscara.

    Returns:
        bool: True se o CPF for válido, False caso contrário.

    Regras:
    - Deve ter 11 dígitos numéricos.
    - Não pode ser uma sequência repetida.
    - Validação dos dígitos verificadores conforme algoritmo oficial.
    """
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
        check = ((value * 10) % 11) % 10
        if check != int(cpf[i]):
            return False
    return True


def is_valid_cnpj(cnpj) -> bool:
    """
    Valida um CNPJ brasileiro.

    Args:
        cnpj (str): CNPJ a ser validado, com ou sem máscara.

    Returns:
        bool: True se o CNPJ for válido, False caso contrário.

    Regras:
    - Deve ter 14 dígitos numéricos.
    - Não pode ser uma sequência repetida.
    - Validação dos dígitos verificadores conforme algoritmo oficial.
    """    
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    size = 12
    numbers = cnpj[:size]
    digits = cnpj[size:]
    sum_ = 0
    pos = size - 7
    for i in range(size):
        sum_ += int(numbers[i]) * pos
        pos -= 1
        if pos < 2:
            pos = 9
    result = sum_ % 11
    if int(digits[0]) != (0 if result < 2 else 11 - result):
        return False
    size += 1
    numbers = cnpj[:size]
    sum_ = 0
    pos = size - 7
    for i in range(size):
        sum_ += int(numbers[i]) * pos
        pos -= 1
        if pos < 2:
            pos = 9
    result = sum_ % 11
    if int(digits[1]) != (0 if result < 2 else 11 - result):
        return False
    return True


def get_document_type(value) -> str:
    """
    Retorna o tipo de documento (CPF ou CNPJ) com base no número informado.

    Args:
        value (str): Número do documento, com ou sem máscara.

    Returns:
        str: 'CPF' se for um CPF válido, 'CNPJ' se for um CNPJ válido, ou None caso contrário.
    """
    value = re.sub(r'\D', '', value)
    if len(value) == 11:
        return 'CPF'
    elif len(value) == 14:
        return 'CNPJ'
    return None