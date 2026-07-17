from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework import status
from production.models import Part, Employee, create_groups

class APIPermissionTests(APITestCase):
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

    def test_anonymous_access_denied(self):
        res = self.client.get('/api/parts/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_view_parts(self):
        self.client.force_authenticate(user=self.wing_worker)
        res = self.client.get('/api/parts/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_wing_worker_produce_part_api(self):
        self.client.force_authenticate(user=self.wing_worker)
        data = {
            'name': 'wing',
            'aircraft_type': 'TB2'
        }
        res = self.client.post('/api/parts/', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.count(), 1)

    def test_wing_worker_unauthorized_produce_api(self):
        self.client.force_authenticate(user=self.wing_worker)
        # Try to produce fuselage part
        data = {
            'name': 'fuselage',
            'aircraft_type': 'TB2'
        }
        res = self.client.post('/api/parts/', data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
