from rest_framework import serializers

from core.models import Solution


class SolutionSerializer(serializers.ModelSerializer):
    """
    solution model serializer
    """
    class Meta:
        model = Solution
        fields = ('id', 'name',)
