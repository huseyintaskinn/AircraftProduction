from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Part, Employee, Assembly


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    model = Part

    list_display = ['name', 'aircraft_type']
    list_filter = ['name', 'aircraft_type']
    search_fields = ['name', 'aircraft_type']
    ordering = ['name', 'aircraft_type']

    fieldsets = (
        (None, {
            'fields': ('name', 'aircraft_type')
        }),
    )


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    model = Employee

    list_display = ['username', 'team']
    list_filter = ['username', 'team']
    search_fields = ['username', 'team']
    ordering = ['username', 'team']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('team',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('team',)}),
    )


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    model = Assembly

    list_display = ['employee', 'aircraft_type', 'is_completed']
    list_filter = ['employee', 'aircraft_type', 'is_completed']
    search_fields = ['employee', 'aircraft_type', 'is_completed']
    ordering = ['employee', 'aircraft_type', 'is_completed']

    fieldsets = (
        (None, {
            'fields': ('employee', 'aircraft_type', 'is_completed')
        }),
        ('Parts', {
            'fields': ('wing', 'fuselage', 'tail', 'avionics')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['wing'].queryset = Part.objects.filter(name='wing')
        form.base_fields['fuselage'].queryset = Part.objects.filter(name='fuselage')
        form.base_fields['tail'].queryset = Part.objects.filter(name='tail')
        form.base_fields['avionics'].queryset = Part.objects.filter(name='avionics')
        return form
