from rest_framework import serializers
from .models import Part, Employee, Assembly


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class AssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assembly
        fields = '__all__'





