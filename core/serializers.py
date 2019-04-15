from rest_framework import serializers

from core.models import Solution, App, Entity, Field


class SolutionSerializer(serializers.ModelSerializer):
    """
    solution model serializer
    """
    class Meta:
        model = Solution
        fields = ('id', 'name',)


class AppSerializer(serializers.ModelSerializer):
    """
    app model serializer
    """
    solution_id = serializers.IntegerField(required=True)

    class Meta:
        model = App
        fields = ('id', 'name', 'solution_id', )


class FieldSerializer(serializers.ModelSerializer):
    """
    entity model serializer
    """
    field_type = serializers.CharField()

    class Meta:
        model = Field
        fields = ('id', 'name', 'field_type',)


class EntitySerializer(serializers.ModelSerializer):
    """
    entity model serializer
    """
    solution_id = serializers.IntegerField(required=True)
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Entity
        fields = ('id', 'name', 'solution_id', 'fields', )


