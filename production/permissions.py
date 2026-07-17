from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import team_to_part_type

class IsAssemblyTeam(BasePermission):
    """
    Allows access only to members of the Assembly Team.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.team == 'assemblyTeam'
        )


class IsProductionTeam(BasePermission):
    """
    Allows access only to members of manufacturing teams (Wing, Fuselage, Tail, Avionics).
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.team in ['wingTeam', 'fuselageTeam', 'tailTeam', 'avionicsTeam']
        )


class TeamBasedPartPermission(BasePermission):
    """
    Allows reading parts for any authenticated user.
    Allows modifications (create, update, delete) only if the employee's team 
    matches the part's type (e.g., Wing Team can only create/update/delete wing parts).
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        # Allow GET/HEAD/OPTIONS for any authenticated employee (e.g., to list parts in UI)
        if request.method in SAFE_METHODS:
            return True

        # For POST, we validate the part type in serializer or checking POST data.
        # But generally, only members of the 4 production teams can write parts.
        return request.user.team in ['wingTeam', 'fuselageTeam', 'tailTeam', 'avionicsTeam']

    def has_object_permission(self, request, view, obj):
        # Allow viewing for all authenticated employees
        if request.method in SAFE_METHODS:
            return True

        # Write actions: check if user team matches part name (e.g. wingTeam -> wing)
        required_part_type = team_to_part_type(request.user.team)
        return obj.name == required_part_type
