from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Part, Assembly, Employee, team_to_part_type, PART_CHOICES, AIRCRAFT_CHOICES

class PartService:
    @staticmethod
    def create_part(employee: Employee, name: str, aircraft_type: str) -> Part:
        """
        Creates a new part. Validates that the employee's team is authorized 
        to produce this type of part.
        """
        required_part_type = team_to_part_type(employee.team)
        
        if not required_part_type:
            raise ValidationError("Bu takım parça üretmeye yetkili değil.")
            
        if name != required_part_type:
            raise ValidationError(
                f"Takımınız ({employee.get_team_display()}) sadece '{required_part_type}' parçası üretebilir. "
                f"'{name}' parçası üretemez."
            )
            
        part = Part.objects.create(
            name=name,
            aircraft_type=aircraft_type,
            created_by=employee
        )
        return part

    @staticmethod
    def recycle_part(part: Part) -> Part:
        """
        Soft deletes (recycles) a part. A part cannot be recycled if it's already used.
        """
        if part.is_used:
            raise ValidationError("Kullanılmış parçalar geri dönüşüme gönderilemez.")
        if part.is_recycled:
            raise ValidationError("Bu parça zaten geri dönüşümde.")
            
        part.is_recycled = True
        part.save()
        return part


class AssemblyService:
    @staticmethod
    @transaction.atomic
    def assemble_aircraft(
        employee: Employee, 
        aircraft_type: str, 
        wing: Part, 
        fuselage: Part, 
        tail: Part, 
        avionics: Part
    ) -> Assembly:
        """
        Assembles an aircraft from 4 parts. Ensures parts compatibility, availability, 
        and marks them as used atomically.
        """
        if employee.team != 'assemblyTeam':
            raise ValidationError("Yalnızca Montaj Takımı personeli uçak montajı yapabilir.")

        # Compatibility validations
        parts = {
            'wing': (wing, 'wing'),
            'fuselage': (fuselage, 'fuselage'),
            'tail': (tail, 'tail'),
            'avionics': (avionics, 'avionics')
        }

        for part_role, (part, expected_name) in parts.items():
            if part.name != expected_name:
                raise ValidationError(f"{part_role.capitalize()} alanına gönderilen parça geçersiz.")
            
            if part.aircraft_type != aircraft_type:
                raise ValidationError(
                    f"Seçilen {expected_name} parçası {part.aircraft_type} tipinde. "
                    f"Bu parça {aircraft_type} uçağı montajında kullanılamaz."
                )
                
            if part.is_used:
                raise ValidationError(f"Seçilen {expected_name} parçası (# {part.id}) zaten başka bir uçakta kullanılmış.")
                
            if part.is_recycled:
                raise ValidationError(f"Seçilen {expected_name} parçası (# {part.id}) geri dönüşümde olduğu için kullanılamaz.")

        # Update parts status
        wing.is_used = True
        fuselage.is_used = True
        tail.is_used = True
        avionics.is_used = True

        wing.save()
        fuselage.save()
        tail.save()
        avionics.save()

        # Create Assembly
        assembly = Assembly.objects.create(
            employee=employee,
            aircraft_type=aircraft_type,
            wing=wing,
            fuselage=fuselage,
            tail=tail,
            avionics=avionics,
            is_completed=True
        )
        return assembly


class InventoryService:
    @staticmethod
    def get_inventory_status():
        """
        Returns active inventory stock counts for all parts grouped by aircraft type
        and calculates missing parts/warnings.
        """
        status = {}
        for ac_code, ac_name in AIRCRAFT_CHOICES:
            parts_info = {}
            for part_code, part_name in PART_CHOICES:
                count = Part.objects.filter(
                    aircraft_type=ac_code,
                    name=part_code,
                    is_used=False,
                    is_recycled=False
                ).count()
                parts_info[part_code] = count
            
            # Find missing parts
            missing = [p_name for p_code, p_name in PART_CHOICES if parts_info[p_code] == 0]
            can_assemble = len(missing) == 0

            status[ac_code] = {
                "name": ac_name,
                "stock": parts_info,
                "can_assemble": can_assemble,
                "missing_parts": missing
            }
        return status
