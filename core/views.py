from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Solution, App, AppVersion, Entity, EntityMap, Branch
from core.serializers import SolutionSerializer, AppSerializer, AppVersionSerializer, EntitySerializer, EntityMapSerializer, BranchSerializer


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

    def get_queryset(self, *args, **kwargs):
        name = self.kwargs.get('name')
        solution_id = self.kwargs.get('solution_id')

        if solution_id and name:
            return App.objects.filter(solution_id=solution_id, name=name)

        return App.objects.all()

class AppVersionView(viewsets.ModelViewSet):
    """
    app version view
    """
    serializer_class = AppVersionSerializer
    queryset = AppVersion.objects.all().order_by('version')

class EntityView(viewsets.ModelViewSet):
    """
    entity model view
    """
    serializer_class = EntitySerializer
    queryset = Entity.objects.all().order_by('name')


class BranchView(viewsets.ModelViewSet):
    """
    branch model view
    """
    serializer_class = BranchSerializer
    queryset = Branch.objects.all().order_by('name')

    def get_queryset(self, *args, **kwargs):
        solution_name = self.kwargs.get('solution_name')
        branch_name = self.kwargs.get('branch_name')

        if solution_name and branch_name:
            return Branch.objects.filter(solution__name=solution_name, name=branch_name)

        return Branch.objects.all()


class EntityMapView(viewsets.ModelViewSet):
    """
    entity model view
    """
    serializer_class = EntityMapSerializer
    queryset = EntityMap.objects.all().order_by('name')

    def get_queryset(self, *args, **kwargs):
        app_name = self.kwargs.get('app_name')
        map_name = self.kwargs.get('map_name')

        if app_name and map_name:
            return EntityMap.objects.filter(app__name=app_name, name=map_name)

        return EntityMap.objects.all()
