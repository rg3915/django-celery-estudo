from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Comando customizado que é chamado via task do Celery.'

    def handle(self, **options):
        self.stdout.write('Comando customizado chamado via task do Celery.')
