from rest_framework.viewsets import ModelViewSet
from .models import Part
from .serializers import PartSerializer


class PartViewSet(ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
