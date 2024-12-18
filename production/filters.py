import django_filters
from .models import Part

PART_TYPES = (
    ('wing', 'Wing'),
    ('fuselage', 'Fuselage'),
    ('tail', 'Tail'),
    ('avionics', 'Avionics'),
)

AIRCRAFT_TYPES = (
    ('TB2', 'TB2'),
    ('TB3', 'TB3'),
    ('AKINCI', 'AKINCI'),
    ('KIZILELMA', 'KIZILELMA'),
)


class PartFilter(django_filters.FilterSet):
    name = django_filters.ChoiceFilter(field_name='name', choices=PART_TYPES, label='Part Type')
    aircraft_type = django_filters.ChoiceFilter(field_name='aircraft_type', choices=AIRCRAFT_TYPES,label='Aircraft Type')
    is_used = django_filters.BooleanFilter(field_name='is_used', label='Is Used')

    class Meta:
        model = Part
        fields = ['name', 'aircraft_type', 'is_used']