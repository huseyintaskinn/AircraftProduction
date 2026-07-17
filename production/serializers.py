from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Part, Employee, Assembly, TEAM_CHOICES, PART_CHOICES, AIRCRAFT_CHOICES
from .services import AssemblyService

class EmployeeSerializer(serializers.ModelSerializer):
    team_display = serializers.CharField(source='get_team_display', read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'team', 'team_display')


class PartSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    aircraft_type_display = serializers.CharField(source='get_aircraft_type_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Part
        fields = (
            'id', 'name', 'name_display', 'aircraft_type', 'aircraft_type_display', 
            'is_used', 'is_recycled', 'created_by', 'created_by_username', 
            'created_at', 'updated_at'
        )
        read_only_fields = ('is_used', 'is_recycled', 'created_by', 'created_at', 'updated_at')


class PartMiniSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)

    class Meta:
        model = Part
        fields = ('id', 'name', 'name_display', 'aircraft_type')


class AssemblySerializer(serializers.ModelSerializer):
    employee_username = serializers.CharField(source='employee.username', read_only=True)
    wing_details = PartMiniSerializer(source='wing', read_only=True)
    fuselage_details = PartMiniSerializer(source='fuselage', read_only=True)
    tail_details = PartMiniSerializer(source='tail', read_only=True)
    avionics_details = PartMiniSerializer(source='avionics', read_only=True)
    aircraft_type_display = serializers.CharField(source='get_aircraft_type_display', read_only=True)

    class Meta:
        model = Assembly
        fields = (
            'id', 'employee', 'employee_username', 'aircraft_type', 'aircraft_type_display',
            'wing', 'wing_details', 'fuselage', 'fuselage_details', 'tail', 'tail_details',
            'avionics', 'avionics_details', 'assembled_at', 'is_completed'
        )
        read_only_fields = ('employee', 'assembled_at', 'is_completed')


class AssemblyCreateSerializer(serializers.Serializer):
    aircraft_type = serializers.ChoiceField(choices=AIRCRAFT_CHOICES)
    wing = serializers.PrimaryKeyRelatedField(queryset=Part.objects.filter(name='wing', is_used=False, is_recycled=False))
    fuselage = serializers.PrimaryKeyRelatedField(queryset=Part.objects.filter(name='fuselage', is_used=False, is_recycled=False))
    tail = serializers.PrimaryKeyRelatedField(queryset=Part.objects.filter(name='tail', is_used=False, is_recycled=False))
    avionics = serializers.PrimaryKeyRelatedField(queryset=Part.objects.filter(name='avionics', is_used=False, is_recycled=False))

    def create(self, validated_data):
        employee = self.context['request'].user
        try:
            assembly = AssemblyService.assemble_aircraft(
                employee=employee,
                aircraft_type=validated_data['aircraft_type'],
                wing=validated_data['wing'],
                fuselage=validated_data['fuselage'],
                tail=validated_data['tail'],
                avionics=validated_data['avionics']
            )
            return assembly
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message)
