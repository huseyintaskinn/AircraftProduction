import django_filters
from .models import Part

class PartFilter(django_filters.FilterSet):
    # Use CharFilter instead of ChoiceFilter to bypass django-filter's choice field bugs in this Python/Django version
    name = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    aircraft_type = django_filters.CharFilter(field_name='aircraft_type', lookup_expr='exact')
    is_used = django_filters.BooleanFilter(field_name='is_used')
    is_recycled = django_filters.BooleanFilter(field_name='is_recycled')

    class Meta:
        model = Part
        fields = ['name', 'aircraft_type', 'is_used', 'is_recycled']