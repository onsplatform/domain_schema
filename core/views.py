from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Solution, App, Entity, EntityMap
from core.serializers import SolutionSerializer, AppSerializer, EntitySerializer, EntityMapSerializer


__all__ = ['SolutionView', 'AppView', 'EntityView', 'EntityMapView', ]


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

    def get_queryset(self, *args, **kwargs):
        app_name = self.kwargs.get('app_name')
        map_name = self.kwargs.get('map_name')

        __import__('ipdb').set_trace()
        if app_name and map_name:
            return EntityMap.objects.filter(app__name=app_name, name=map_name)

        return EntityMap.objects.all()
