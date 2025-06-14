import pytest
from agric.validators import is_valid_cpf, is_valid_cnpj, get_document_type

# CPFs válidos e inválidos para teste
VALID_CPF = "12345678909"
INVALID_CPF = "12345678900"
REPEATED_CPF = "11111111111"

# CNPJs válidos e inválidos para teste
VALID_CNPJ = "11222333000181"
INVALID_CNPJ = "11222333000100"
REPEATED_CNPJ = "22222222222222"

def test_is_valid_cpf_valido():
    assert is_valid_cpf(VALID_CPF) is True

def test_is_valid_cpf_invalido():
    assert is_valid_cpf(INVALID_CPF) is False

def test_is_valid_cpf_repetido():
    assert is_valid_cpf(REPEATED_CPF) is False

def test_is_valid_cpf_com_mascara():
    assert is_valid_cpf("123.456.789-09") is True

def test_is_valid_cpf_tamanho_errado():
    assert is_valid_cpf("12345678") is False

def test_is_valid_cnpj_valido():
    assert is_valid_cnpj(VALID_CNPJ) is True

def test_is_valid_cnpj_invalido():
    assert is_valid_cnpj(INVALID_CNPJ) is False

def test_is_valid_cnpj_repetido():
    assert is_valid_cnpj(REPEATED_CNPJ) is False

def test_is_valid_cnpj_com_mascara():
    assert is_valid_cnpj("11.222.333/0001-81") is True

def test_is_valid_cnpj_tamanho_errado():
    assert is_valid_cnpj("11222333") is False

def test_get_document_type_cpf():
    assert get_document_type(VALID_CPF) == "CPF"
    assert get_document_type("123.456.789-09") == "CPF"

def test_get_document_type_cnpj():
    assert get_document_type(VALID_CNPJ) == "CNPJ"
    assert get_document_type("11.222.333/0001-81") == "CNPJ"

def test_get_document_type_invalido():
    assert get_document_type("123") is None
    assert get_document_type("") is None
    assert get_document_type("abc") is None
    