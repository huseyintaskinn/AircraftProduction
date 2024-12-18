from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .models import Part, Employee, Assembly
from .serializers import PartSerializer, EmployeeSerializer, AssemblySerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PartFilter
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@extend_schema_view(
    list=extend_schema(
        summary="List all parts",
        description="Retrieve a list of all parts available in the system.",
        tags=["Parts"],
        responses={200: PartSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a single part",
        description="Get detailed information about a specific part by its ID.",
        tags=["Parts"],
        responses={200: PartSerializer},
    ),
    create=extend_schema(
        summary="Create a new part",
        description="Add a new part to the system by providing the required details.",
        tags=["Parts"],
        request=PartSerializer,
        responses={201: PartSerializer},
    ),
    update=extend_schema(
        summary="Update an existing part",
        description="Modify the details of an existing part by providing its ID.",
        tags=["Parts"],
        request=PartSerializer,
        responses={200: PartSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update a part",
        description="Update specific fields of a part by its ID.",
        tags=["Parts"],
        request=PartSerializer,
        responses={200: PartSerializer},
    ),
    destroy=extend_schema(
        summary="Delete a part",
        description="Remove a part from the system by its ID.",
        tags=["Parts"],
        responses={204: None},
    ),
)
class PartViewSet(ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartFilter


@extend_schema_view(
    list=extend_schema(
        summary="List all employees",
        description="Retrieve a list of all employees.",
        tags=["Employees"],
        responses={200: EmployeeSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve an employee",
        description="Get detailed information about a specific employee.",
        tags=["Employees"],
        responses={200: EmployeeSerializer},
    ),
    create=extend_schema(
        summary="Create a new employee",
        description="Add a new employee to the system.",
        tags=["Employees"],
        request=EmployeeSerializer,
        responses={201: EmployeeSerializer},
    ),
    update=extend_schema(
        summary="Update an employee",
        description="Update the details of an existing employee.",
        tags=["Employees"],
        request=EmployeeSerializer,
        responses={200: EmployeeSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update an employee",
        description="Modify specific fields of an employee.",
        tags=["Employees"],
        request=EmployeeSerializer,
        responses={200: EmployeeSerializer},
    ),
    destroy=extend_schema(
        summary="Delete an employee",
        description="Remove an employee from the system.",
        tags=["Employees"],
        responses={204: None},
    ),
)
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema_view(
    list=extend_schema(
        summary="List all assemblies",
        description="Retrieve a list of all assemblies in the system.",
        tags=["Assemblies"],
        responses={200: AssemblySerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve an assembly",
        description="Get detailed information about a specific assembly.",
        tags=["Assemblies"],
        responses={200: AssemblySerializer},
    ),
    create=extend_schema(
        summary="Create a new assembly",
        description="Add a new assembly with the required details.",
        tags=["Assemblies"],
        request=AssemblySerializer,
        responses={201: AssemblySerializer},
    ),
    update=extend_schema(
        summary="Update an assembly",
        description="Modify the details of an existing assembly.",
        tags=["Assemblies"],
        request=AssemblySerializer,
        responses={200: AssemblySerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update an assembly",
        description="Update specific fields of an assembly.",
        tags=["Assemblies"],
        request=AssemblySerializer,
        responses={200: AssemblySerializer},
    ),
    destroy=extend_schema(
        summary="Delete an assembly",
        description="Remove an assembly from the system.",
        tags=["Assemblies"],
        responses={204: None},
    ),
)
class AssemblyViewSet(ModelViewSet):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    permission_classes = [IsAuthenticated, IsAssemblyTeam]

@extend_schema_view(
        retrieve=extend_schema(
            summary="Retrieve user information",
            description="Get detailed information about the currently logged-in user.",
            tags=["User"],
            responses={200: EmployeeSerializer},
        ),
    )
class UserDataView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')
