import re

def is_valid_cpf(cpf) -> bool:
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
    value = re.sub(r'\D', '', value)
    if len(value) == 11:
        return 'CPF'
    elif len(value) == 14:
        return 'CNPJ'
    return None