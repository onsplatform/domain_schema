from rest_framework import viewsets

from core.models import Solution, App
from core.serializers import SolutionSerializer, AppSerializer


__all__ = ['SolutionView', 'AppView', ]


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
