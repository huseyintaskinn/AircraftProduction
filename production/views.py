from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as APIValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Part, Employee, Assembly
from .serializers import (
    PartSerializer, EmployeeSerializer, AssemblySerializer, AssemblyCreateSerializer
)
from .permissions import IsAssemblyTeam, TeamBasedPartPermission
from .filters import PartFilter
from .services import PartService, InventoryService

@extend_schema_view(
    list=extend_schema(
        summary="List all active parts",
        description="Retrieve a list of all non-recycled parts by default. Pass include_recycled=true to see recycled.",
        tags=["Parts"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a single part",
        description="Get detailed information about a specific part by its ID.",
        tags=["Parts"],
    ),
    create=extend_schema(
        summary="Create a new part",
        description="Add a new part to the system. Must match the employee's team type (e.g. wing team creates wing part).",
        tags=["Parts"],
    ),
    update=extend_schema(
        summary="Update an existing part",
        description="Modify the details of an existing part.",
        tags=["Parts"],
    ),
    partial_update=extend_schema(
        summary="Partially update a part",
        description="Update specific fields of a part.",
        tags=["Parts"],
    ),
    destroy=extend_schema(
        summary="Recycle (delete) a part",
        description="Marks a part as recycled (is_recycled=True). Fails if the part is already used in an aircraft.",
        tags=["Parts"],
    ),
)
class PartViewSet(ModelViewSet):
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated, TeamBasedPartPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartFilter

    def get_queryset(self):
        queryset = Part.objects.all()
        # By default exclude recycled parts
        include_recycled = self.request.query_params.get('include_recycled', 'false').lower() == 'true'
        if not include_recycled:
            queryset = queryset.filter(is_recycled=False)
        return queryset

    def perform_create(self, serializer):
        try:
            PartService.create_part(
                employee=self.request.user,
                name=serializer.validated_data['name'],
                aircraft_type=serializer.validated_data['aircraft_type']
            )
        except DjangoValidationError as e:
            raise APIValidationError(e.message)

    def destroy(self, request, *args, **kwargs):
        part = self.get_object()
        try:
            PartService.recycle_part(part)
            return Response({"detail": "Parça başarıyla geri dönüşüme gönderildi."}, status=status.HTTP_200_OK)
        except DjangoValidationError as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        summary="List all employees",
        tags=["Employees"],
    ),
    retrieve=extend_schema(
        summary="Retrieve an employee",
        tags=["Employees"],
    ),
    create=extend_schema(
        summary="Create a new employee",
        tags=["Employees"],
    ),
    update=extend_schema(
        summary="Update an employee",
        tags=["Employees"],
    ),
    partial_update=extend_schema(
        summary="Partially update an employee",
        tags=["Employees"],
    ),
    destroy=extend_schema(
        summary="Delete an employee",
        tags=["Employees"],
    ),
)
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema_view(
    list=extend_schema(
        summary="List all assembled aircrafts",
        tags=["Assemblies"],
    ),
    retrieve=extend_schema(
        summary="Retrieve assembled aircraft details",
        tags=["Assemblies"],
    ),
    create=extend_schema(
        summary="Assemble a new aircraft",
        description="Combine a Wing, Fuselage, Tail, and Avionics part of the same aircraft type into a new aircraft.",
        tags=["Assemblies"],
        request=AssemblyCreateSerializer,
    ),
)
class AssemblyViewSet(ModelViewSet):
    queryset = Assembly.objects.all()
    permission_classes = [IsAuthenticated, IsAssemblyTeam]

    def get_serializer_class(self):
        if self.action == 'create':
            return AssemblyCreateSerializer
        return AssemblySerializer


class UserDataView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Retrieve current user profile",
        tags=["User"],
        responses={200: EmployeeSerializer},
    )
    def get(self, request):
        serializer = self.serializer_class(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Retrieve active inventory counts and missing parts warnings",
        tags=["Inventory"],
    )
    def get(self, request):
        status_data = InventoryService.get_inventory_status()
        return Response(status_data, status=status.HTTP_200_OK)
