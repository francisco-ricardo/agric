import pytest
from django.core.exceptions import ValidationError
from agric.models import Produtor, Estado, Cidade, TipoCultura, Propriedade, Cultura

@pytest.mark.django_db
class TestModels:

    def test_produtor_cpf_valido(self):
        produtor = Produtor(cpf_cnpj="12345678909", nome_produtor="Produtor CPF", tipo_documento="CPF")
        produtor.save()
        assert produtor.tipo_documento == "CPF"
        assert str(produtor) == "Produtor CPF (12345678909)"

    def test_produtor_cnpj_valido(self):
        produtor = Produtor(cpf_cnpj="11222333000181", nome_produtor="Produtor CNPJ", tipo_documento="CNPJ")
        produtor.save()
        assert produtor.tipo_documento == "CNPJ"
        assert str(produtor) == "Produtor CNPJ (11222333000181)"

    def test_produtor_documento_invalido(self):
        produtor = Produtor(cpf_cnpj="123", nome_produtor="Inválido", tipo_documento="CPF")
        with pytest.raises(ValidationError):
            produtor.save()

    def test_estado_unique(self):
        estado = Estado.objects.create(nome_estado="Minas Gerais")
        assert str(estado) == "Minas Gerais"
        with pytest.raises(Exception):
            Estado.objects.create(nome_estado="Minas Gerais")

    def test_cidade_unique_together(self):
        estado = Estado.objects.create(nome_estado="Bahia")
        cidade1 = Cidade.objects.create(nome_cidade="Salvador", estado=estado)
        assert str(cidade1) == "Salvador (Bahia)"
        with pytest.raises(Exception):
            Cidade.objects.create(nome_cidade="Salvador", estado=estado)

    def test_tipocultura_unique(self):
        tipo = TipoCultura.objects.create(tipo_cultura="Soja")
        assert str(tipo) == "Soja"
        with pytest.raises(Exception):
            TipoCultura.objects.create(tipo_cultura="Soja")

    def test_propriedade_area_valida(self):
        estado = Estado.objects.create(nome_estado="Paraná")
        cidade = Cidade.objects.create(nome_cidade="Curitiba", estado=estado)
        produtor = Produtor.objects.create(cpf_cnpj="98765432100", nome_produtor="Produtor", tipo_documento="CPF")
        prop = Propriedade(
            nome_propriedade="Fazenda 1",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            cidade=cidade,
            produtor=produtor
        )
        prop.save()
        assert str(prop) == "Fazenda 1"

    def test_propriedade_area_invalida(self):
        estado = Estado.objects.create(nome_estado="SP")
        cidade = Cidade.objects.create(nome_cidade="Campinas", estado=estado)
        produtor = Produtor.objects.create(cpf_cnpj="98765432100", nome_produtor="Produtor", tipo_documento="CPF")
        prop = Propriedade(
            nome_propriedade="Fazenda Inválida",
            area_total=100.0,
            area_agricultavel=80.0,
            area_vegetacao=30.0,
            cidade=cidade,
            produtor=produtor
        )
        with pytest.raises(ValidationError):
            prop.full_clean()

    def test_cultura_unique_together(self):
        estado = Estado.objects.create(nome_estado="RS")
        cidade = Cidade.objects.create(nome_cidade="Porto Alegre", estado=estado)
        produtor = Produtor.objects.create(cpf_cnpj="12345678909", nome_produtor="Produtor", tipo_documento="CPF")
        prop = Propriedade.objects.create(
            nome_propriedade="Fazenda Cultura",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            cidade=cidade,
            produtor=produtor
        )
        tipo = TipoCultura.objects.create(tipo_cultura="Milho")
        cultura1 = Cultura.objects.create(
            ano_safra=2025,
            tipo_cultura=tipo,
            propriedade=prop
        )
        assert str(cultura1) == "Milho - 2025 (Fazenda Cultura)"
        with pytest.raises(Exception):
            Cultura.objects.create(
                ano_safra=2025,
                tipo_cultura=tipo,
                propriedade=prop
            )
            