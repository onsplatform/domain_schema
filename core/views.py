from rest_framework import viewsets

from core.models import Solution
from core.serializers import SolutionSerializer


__all__ = ['SolutionView', ]


class SolutionView(viewsets.ModelViewSet):
    """
    solution model view
    """
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all().order_by('name')
