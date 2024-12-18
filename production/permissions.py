from rest_framework.permissions import BasePermission


class IsAssemblyTeam(BasePermission):
    def has_permission(self, request, view):
        return request.user.team == 'assemblyTeam'

    def has_object_permission(self, request, view, obj):
        return request.user.team == 'assemblyTeam'


class IsWingTeam(BasePermission):
    def has_permission(self, request, view):
        return request.user.team == 'wingTeam'

    def has_object_permission(self, request, view, obj):
        return request.user.team == 'wingTeam'


class IsFuselageTeam(BasePermission):
    def has_permission(self, request, view):
        return request.user.team == 'fuselageTeam'

    def has_object_permission(self, request, view, obj):
        return request.user.team == 'fuselageTeam'


class IsTailTeam(BasePermission):
    def has_permission(self, request, view):
        return request.user.team == 'tailTeam'

    def has_object_permission(self, request, view, obj):
        return request.user.team == 'tailTeam'


class IsAvionicsTeam(BasePermission):
    def has_permission(self, request, view):
        return request.user.team == 'avionicsTeam'

    def has_object_permission(self, request, view, obj):
        return request.user.team == 'avionicsTeam'

