from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Part, Employee, Assembly


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    model = Part

    list_display = ['id', 'name', 'aircraft_type', 'is_used', 'is_recycled', 'created_by', 'created_at']
    list_filter = ['name', 'aircraft_type', 'is_used', 'is_recycled']
    search_fields = ['created_by__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'aircraft_type', 'is_used', 'is_recycled', 'created_by')
        }),
        ('Zaman Bilgileri', {
            'fields': ('created_at', 'updated_at')
        })
    )


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    model = Employee

    list_display = ['username', 'email', 'team', 'is_staff']
    list_filter = ['team', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('Takım Ayarları', {'fields': ('team',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Takım Ayarları', {'fields': ('team',)}),
    )


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    model = Assembly

    list_display = ['id', 'employee', 'aircraft_type', 'assembled_at', 'is_completed']
    list_filter = ['aircraft_type', 'is_completed']
    search_fields = ['employee__username']
    ordering = ['-assembled_at']
    readonly_fields = ['assembled_at']

    fieldsets = (
        (None, {
            'fields': ('employee', 'aircraft_type', 'is_completed', 'assembled_at')
        }),
        ('Kullanılan Parçalar', {
            'fields': ('wing', 'fuselage', 'tail', 'avionics')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filter dropdown to show only corresponding parts that are not used/recycled (or currently selected parts)
        form.base_fields['wing'].queryset = Part.objects.filter(name='wing')
        form.base_fields['fuselage'].queryset = Part.objects.filter(name='fuselage')
        form.base_fields['tail'].queryset = Part.objects.filter(name='tail')
        form.base_fields['avionics'].queryset = Part.objects.filter(name='avionics')
        return form
