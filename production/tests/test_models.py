from django.test import TestCase
from production.models import Part, Employee, Assembly, create_groups

class ModelTests(TestCase):
    def setUp(self):
        create_groups()
        self.wing_worker = Employee.objects.create_user(
            username='wing_worker', 
            password='testpassword', 
            team='wingTeam'
        )
        self.assembly_worker = Employee.objects.create_user(
            username='assembly_worker', 
            password='testpassword', 
            team='assemblyTeam'
        )

    def test_employee_creation_and_groups(self):
        # Assert group auto-assignment works
        self.assertTrue(self.wing_worker.groups.filter(name='Kanat Takımı').exists())
        self.assertTrue(self.assembly_worker.groups.filter(name='Montaj Takımı').exists())

    def test_part_creation_defaults(self):
        part = Part.objects.create(
            name='wing',
            aircraft_type='TB2',
            created_by=self.wing_worker
        )
        self.assertEqual(part.name, 'wing')
        self.assertEqual(part.aircraft_type, 'TB2')
        self.assertFalse(part.is_used)
        self.assertFalse(part.is_recycled)
