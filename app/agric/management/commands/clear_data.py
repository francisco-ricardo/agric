from django.core.management.base import BaseCommand
from agric.models import Estado, Cidade, TipoCultura, Produtor, Propriedade, Cultura

class Command(BaseCommand):
    
    help = "Remove todos os dados das tabelas principais do app agric"

    def handle(self, *args, **kwargs):
        self.stdout.write("Removendo dados das tabelas...")
        Cultura.objects.all().delete()
        Propriedade.objects.all().delete()
        Produtor.objects.all().delete()
        TipoCultura.objects.all().delete()
        Cidade.objects.all().delete()
        Estado.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Dados removidos com sucesso!"))
