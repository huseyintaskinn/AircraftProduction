from django.core.management.base import BaseCommand
from production.models import create_groups


class Command(BaseCommand):
    help = 'Bir kerelik grup oluşturur'

    def handle(self, *args, **kwargs):
        try:
            groups = create_groups()
            self.stdout.write(self.style.SUCCESS('Gruplar başarıyla oluşturuldu:'))
            for group in groups:
                self.stdout.write(f"- {group.name}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hata oluştu: {str(e)}'))
