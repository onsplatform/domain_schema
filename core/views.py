from rest_framework import viewsets

from core.models import Solution, App, Entity, EntityMap
from core.serializers import SolutionSerializer, AppSerializer, EntitySerializer, EntityMapSerializer


__all__ = ['SolutionView', 'AppView', 'EntityView' ]


class SolutionView(viewsets.ModelViewSet):
    """
    solution model view
    """
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all().order_by('name')


class AppView(viewsets.ModelViewSet):
    """
    app model view
    """
    serializer_class = AppSerializer
    queryset = App.objects.all().order_by('name')


class EntityView(viewsets.ModelViewSet):
    """
    entity model view
    """
    serializer_class = EntitySerializer
    queryset = Entity.objects.all().order_by('name')


class EntityMapView(viewsets.ModelViewSet):
    """
    entity model view
    """
    serializer_class = EntityMapSerializer
    queryset = EntityMap.objects.all().order_by('name')
