from rest_framework.viewsets import ModelViewSet
from .serializers import ComponentDetailSerializer
from .models import GrossularCustomUMLComponent


class ComponentViewSet(ModelViewSet):
    queryset = GrossularCustomUMLComponent.objects.all()
    serializer_class = ComponentDetailSerializer

