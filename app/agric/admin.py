from django.contrib import admin
from .models import Produtor

@admin.register(Produtor)
class ProdutorAdmin(admin.ModelAdmin):
    list_display = ("cpf_cnpj", "tipo_documento", "nome_produtor")
    search_fields = ("cpf_cnpj", "nome_produtor")
