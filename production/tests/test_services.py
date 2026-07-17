from django.test import TestCase
from django.core.exceptions import ValidationError
from production.models import Part, Employee, create_groups
from production.services import PartService, AssemblyService, InventoryService

class ServiceTests(TestCase):
    def setUp(self):
        create_groups()
        self.wing_worker = Employee.objects.create_user(
            username='wing_worker', 
            password='testpassword', 
            team='wingTeam'
        )
        self.fuselage_worker = Employee.objects.create_user(
            username='fuselage_worker', 
            password='testpassword', 
            team='fuselageTeam'
        )
        self.tail_worker = Employee.objects.create_user(
            username='tail_worker', 
            password='testpassword', 
            team='tailTeam'
        )
        self.avionics_worker = Employee.objects.create_user(
            username='avionics_worker', 
            password='testpassword', 
            team='avionicsTeam'
        )
        self.assembly_worker = Employee.objects.create_user(
            username='assembly_worker', 
            password='testpassword', 
            team='assemblyTeam'
        )

    def test_part_production_restrictions(self):
        # Wing worker can produce wing part
        part = PartService.create_part(self.wing_worker, 'wing', 'TB2')
        self.assertEqual(part.name, 'wing')

        # Wing worker cannot produce fuselage part
        with self.assertRaises(ValidationError):
            PartService.create_part(self.wing_worker, 'fuselage', 'TB2')

    def test_recycle_used_part_fails(self):
        part = PartService.create_part(self.wing_worker, 'wing', 'TB2')
        part.is_used = True
        part.save()

        # Cannot recycle used part
        with self.assertRaises(ValidationError):
            PartService.recycle_part(part)

    def test_valid_assembly(self):
        wing = PartService.create_part(self.wing_worker, 'wing', 'TB2')
        fuselage = PartService.create_part(self.fuselage_worker, 'fuselage', 'TB2')
        tail = PartService.create_part(self.tail_worker, 'tail', 'TB2')
        avionics = PartService.create_part(self.avionics_worker, 'avionics', 'TB2')

        # Valid assembly
        assembly = AssemblyService.assemble_aircraft(
            employee=self.assembly_worker,
            aircraft_type='TB2',
            wing=wing,
            fuselage=fuselage,
            tail=tail,
            avionics=avionics
        )
        self.assertTrue(assembly.is_completed)
        
        # Verify parts are marked as used
        wing.refresh_from_db()
        self.assertTrue(wing.is_used)

    def test_invalid_assembly_incompatible_aircraft_type(self):
        wing = PartService.create_part(self.wing_worker, 'wing', 'TB2')
        fuselage = PartService.create_part(self.fuselage_worker, 'fuselage', 'TB3') # Incompatible
        tail = PartService.create_part(self.tail_worker, 'tail', 'TB2')
        avionics = PartService.create_part(self.avionics_worker, 'avionics', 'TB2')

        with self.assertRaises(ValidationError):
            AssemblyService.assemble_aircraft(
                employee=self.assembly_worker,
                aircraft_type='TB2',
                wing=wing,
                fuselage=fuselage,
                tail=tail,
                avionics=avionics
            )

    def test_inventory_missing_parts(self):
        # Empty inventory initially
        inv = InventoryService.get_inventory_status()
        self.assertFalse(inv['TB2']['can_assemble'])
        self.assertIn('Kanat', inv['TB2']['missing_parts'])

        # Produce all parts for TB2
        PartService.create_part(self.wing_worker, 'wing', 'TB2')
        PartService.create_part(self.fuselage_worker, 'fuselage', 'TB2')
        PartService.create_part(self.tail_worker, 'tail', 'TB2')
        PartService.create_part(self.avionics_worker, 'avionics', 'TB2')

        inv = InventoryService.get_inventory_status()
        self.assertTrue(inv['TB2']['can_assemble'])
        self.assertEqual(len(inv['TB2']['missing_parts']), 0)
