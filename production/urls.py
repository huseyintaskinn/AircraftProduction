from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartViewSet, EmployeeViewSet, AssemblyViewSet, UserDataView, InventoryStatusView


router = DefaultRouter()
router.register(r'parts', PartViewSet, basename='part')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'assemblies', AssemblyViewSet, basename='assembly')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserDataView.as_view(), name='user-data'),
    path('inventory/', InventoryStatusView.as_view(), name='inventory-status'),
]