from rest_framework.viewsets import ModelViewSet
from .serializers import ComponentDetailSerializer, InterfaceSerializer
from .models import GrossularCustomUMLComponent, GrossularCustomUMLComponentInterface
from django_filters import rest_framework as filters


class ComponentViewSet(ModelViewSet):
    queryset = GrossularCustomUMLComponent.objects.all()
    serializer_class = ComponentDetailSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('grossularProject__codeName','package__name','name','codeName')


class InterfaceViewSet(ModelViewSet):
    queryset = GrossularCustomUMLComponentInterface.objects.all()
    serializer_class = InterfaceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('grossularProject__codeName', 'Component__package__name', 'Component__codeName', 'name')
