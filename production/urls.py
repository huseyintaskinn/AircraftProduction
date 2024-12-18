from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartViewSet, EmployeeViewSet, AssemblyViewSet, UserDataView


router = DefaultRouter()
router.register(r'parts', PartViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'assemblies', AssemblyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserDataView.as_view(), name='user-data'),
]