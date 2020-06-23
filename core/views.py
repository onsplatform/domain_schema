import yaml
import pytz
import datetime

from collections import defaultdict

from django.db.models import Q
from django.db.models import Subquery
from django.http import HttpResponse

from core.management.commands.import_data import EntityLoader
from core.management.commands.import_map import MapLoader

from rest_framework import viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from core.models import Solution, App, AppVersion, Entity, EntityMap, Branch, Reprocess, Reproduction
from core.serializers import SolutionSerializer, AppSerializer, AppVersionSerializer, EntitySerializer, \
    EntityMapSerializer, BranchSerializer, ReprocessSerializer, ReproductionSerializer

__all__ = ['SolutionView', 'AppView', 'EntityView', 'EntityMapView', ]


class SolutionView(viewsets.ModelViewSet):
    """
    solution model view
    """
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all().order_by('name')

    def get_queryset(self, *args, **kwargs):
        solution_name = self.kwargs.get('solution_name')

        if solution_name:
            return Solution.objects.filter(name=solution_name)

        return Solution.objects.all()


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
    queryset = AppVersion.objects.all().order_by('-date_begin_validity')

    def get_queryset(self, *args, **kwargs):
        date_validity = self.kwargs.get('date_validity')
        process_id = self.kwargs.get('process_id')
        app_name = self.kwargs.get('app_name')
        version = self.kwargs.get('version')

        if app_name and version:
            return AppVersion.objects.filter(app__name=app_name, version=version)

        if process_id and date_validity:
            date_validity = datetime.datetime.strptime(date_validity, '%Y-%m-%dT%H:%M:%S.%fZ')
            pst = pytz.timezone('UTC')
            date_validity = pst.localize(date_validity)

            return AppVersion.objects.filter(process_id=process_id) \
                .filter(date_begin_validity__lte=date_validity) \
                .filter(Q(date_end_validity__isnull=True) | Q(date_end_validity__gte=date_validity)) \
                .order_by('-date_begin_validity')

        return AppVersion.objects.all().order_by('-date_begin_validity')


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

    def update(self, request, *args, **kwargs):
        if request.data['disabled'] and request.data['name'] == 'master':
            return HttpResponse(status=409, reason="It is not allowed to disable branch master")
        else:
            return super().update(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        solution_name = self.kwargs.get('solution_name')
        branch_name = self.kwargs.get('branch_name')

        if solution_name and branch_name:
            solution = Solution.objects.get(name=solution_name)
            return Branch.objects.filter(solution_id=solution.id, name=branch_name)
        if branch_name:
            return Branch.objects.filter(name=branch_name)

        return Branch.objects.all()


class UpsertExecutionView(views.APIView):

    def upsert(self, action, execution, new_execution, execution_attr):
        if action not in ['start', 'finish']:
            return False

        if execution is None:
            execution = new_execution
        setattr(execution, execution_attr, action == 'start')
        execution.save()
        return True


class UpsertReproductionView(UpsertExecutionView):
    """
    reproduction model view
    """
    serializer_class = ReproductionSerializer

    def post(self, request):
        tag = request.data['tag']
        action = request.data['action']
        solution = request.data['solution']
        reproduction_instance_id = request.data['reproduction_instance_id']

        execution = Reproduction.objects.filter(solution_id=solution, tag=tag,
                                                reproduction_instance_id=reproduction_instance_id).first()
        new_execution = Reproduction(solution_id=solution, tag=tag, reproduction_instance_id=reproduction_instance_id,
                                     is_reproducing=True)
        if self.upsert(action, execution, new_execution, 'is_reproducing'):
            return Response(status=200)

        return Response(status=500)


class UpsertReprocessView(UpsertExecutionView):
    """
    reprocess model view
    """
    serializer_class = ReprocessSerializer

    def post(self, request):
        tag = request.data['tag']
        action = request.data['action']
        solution = request.data['solution']
        reprocess_instance_id = request.data['reprocess_instance_id']

        execution = Reprocess.objects.filter(solution_id=solution, tag=tag,
                                             reprocess_instance_id=reprocess_instance_id).first()
        new_execution = Reprocess(solution_id=solution, tag=tag, reprocess_instance_id=reprocess_instance_id,
                                  is_reprocessing=True)
        if self.upsert(action, execution, new_execution, 'is_reprocessing'):
            return Response(status=200)

        Response(status=500)


class ReprocessView(viewsets.ModelViewSet):
    """
    reprocess model view
    """
    serializer_class = ReprocessSerializer
    queryset = Reprocess.objects.all().order_by('id')

    def get_queryset(self, *args, **kwargs):
        solution_id = self.kwargs.get('solution_id')
        return Reprocess.objects.filter(solution_id=solution_id, is_reprocessing=True) \
            .values('tag', 'reprocess_instance_id', 'is_running')


class ReproductionView(viewsets.ModelViewSet):
    """
    reproduction model view
    """
    serializer_class = ReproductionSerializer
    queryset = Reproduction.objects.all().order_by('id')

    def get_queryset(self, *args, **kwargs):
        solution_id = self.kwargs.get('solution_id')
        return Reproduction.objects.filter(solution_id=solution_id, is_reproducing=True) \
            .values('tag', 'reproduction_instance_id', 'is_reproducing')


class EntityMapView(viewsets.ModelViewSet):
    """
    entity model view
    """
    serializer_class = EntityMapSerializer
    queryset = EntityMap.objects.all().order_by('name')

    def get_queryset(self, *args, **kwargs):
        app_name = self.kwargs.get('app_name')
        app_version = self.kwargs.get('app_version')
        map_name = self.kwargs.get('map_name')

        if app_name and map_name and app_version:
            return EntityMap.objects.filter(app_version__app__name=app_name, app_version__version=app_version,
                                            name=map_name)

        return EntityMap.objects.all()


class AppVersionByReprocessableEntityView(views.APIView):
    """
    App_version by reprocessable entities
    {
        "types": [
            "parametrotaxa",
            "eventomudancaestadooperativo",
            "potenciaunidadegeradora"
        ],
        "tag": "onssagercalculouge:1.0"
    }

    return:
    {
        "onssagercalculouge:1.0": [
            "e_potuge",
            "e_eventomudaestdopert"
        ],
        "onssagercalculouge:2.0": [
            "e_potuge"
        ]
    }
    """

    def post(self, request):
        tag = request.data['tag']
        types = request.data['types']

        tables = EntityMap.objects.filter(name__in=types, app_version__tag=tag).values('entity__name')

        app_versions = [
            (e['app_version__tag'], e['entity__name'])
            for e in EntityMap.objects.filter(reprocessable=True, entity__name__in=Subquery(tables)).values(
                'app_version__tag', 'entity__name')
        ]

        dic = defaultdict(set)
        for k, v in app_versions:
            dic[k].update(v.split(','))

        return Response(data=dic, status=200)


class CreateEntityView(views.APIView):
    """
    upload metadata view
    """

    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.FILES
        solution = Solution.objects.get(name=request.data['solution'])
        loader = EntityLoader()

        for file in file_obj:
            yaml_dict = yaml.load(file_obj[file], Loader=yaml.FullLoader)
            loader.create_entity(yaml_dict, solution)

        return Response(status=200)


class CreateMapMapView(views.APIView):
    """
    upload maps view
    """

    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.FILES
        app_name = request.data['app']
        app_version = request.data['app_version']
        loader = MapLoader()

        for file in file_obj:
            yaml_dict = yaml.load(file_obj[file], Loader=yaml.FullLoader)
            loader.create_maps(yaml_dict, app_name, app_version)

        return Response(status=200)
