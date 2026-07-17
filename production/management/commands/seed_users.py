from django.core.management.base import BaseCommand
from production.models import Employee, create_groups

class Command(BaseCommand):
    help = 'Seeds database with default employees for testing purposes'

    def handle(self, *args, **options):
        # Make sure groups are created first
        create_groups()

        users_to_create = [
            ('wing_worker', 'wingTeam'),
            ('fuselage_worker', 'fuselageTeam'),
            ('tail_worker', 'tailTeam'),
            ('avionics_worker', 'avionicsTeam'),
            ('assembly_worker', 'assemblyTeam'),
        ]

        self.stdout.write("Seeding employees...")
        for username, team in users_to_create:
            if not Employee.objects.filter(username=username).exists():
                emp = Employee.objects.create_user(
                    username=username,
                    password='testpassword',
                    email=f'{username}@baykar.com',
                    team=team
                )
                self.stdout.write(self.style.SUCCESS(f"Employee '{username}' ({team}) successfully created!"))
            else:
                self.stdout.write(f"Employee '{username}' already exists.")
        
        # Create superuser (admin) if not exists
        if not Employee.objects.filter(username='admin').exists():
            Employee.objects.create_superuser(
                username='admin',
                password='adminpassword',
                email='admin@baykar.com',
                team='assemblyTeam'
            )
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' successfully created!"))
            
        self.stdout.write(self.style.SUCCESS("Database seeding completed! Password for workers: testpassword, for admin: adminpassword"))
