from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core import management
from rest_framework.views import APIView
from rest_framework import status
from core.models import Solution, App, AppVersion, Entity, EntityMap, Branch
from core.serializers import SolutionSerializer, AppSerializer, AppVersionSerializer, EntitySerializer, EntityMapSerializer, BranchSerializer
import json

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


class ImportDataView(APIView):

    def post(self, request):
        """
        Loads the yaml files and create the domain.
        SAMPLE URL: http://127.0.0.1:8000/api/v1/import_data/
        {
            "path": "D:\\_PLATFORM\\sager\\Dominio",
            "solution": "Sager"
        }
        """
        try:
            assert (request.POST.get('_content') is not ''), "Request contains no data: " + str(request.POST)
            result = json.loads(request.POST.get('_content'))
            path = result.get('path')
            solution = result.get('solution')

            management.call_command("import_data", path, solution)

            return Response('Success', status=status.HTTP_201_CREATED)
        except AssertionError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response('ERROR => ' + str(ex), status=status.HTTP_400_BAD_REQUEST)


class ImportMapView(APIView):

    def post(self, request):
        """
        Loads the yaml files and create the maps.
        SAMPLE URL: http://127.0.0.1:8000/api/v1/import_map/
        """
        try:
            result = json.loads(request.POST.get('_content'))

            path = result.get('path')
            solution = result.get('solution')
            app = result.get('app')

            management.call_command("import_map", path, solution, app)

            return Response('Success', status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response('ERROR => ' + str(ex), status=status.HTTP_400_BAD_REQUEST)