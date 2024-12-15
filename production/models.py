from django.db import models


class Part(models.Model):
    name = models.CharField(max_length=100)
    aircraft_type = models.CharField(max_length=100)  # Örn: TB2, TB3


class Team(models.Model):
    name = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)  # Örn: Kanat, Gövde


class Employee(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)