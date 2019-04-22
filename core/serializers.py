from rest_framework import serializers

from drf_writable_nested import WritableNestedModelSerializer

from core.models import Solution, App, Entity, Field, EntityMap


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
        fields = ('pk', 'name', 'field_type',)


class EntitySerializer(WritableNestedModelSerializer):
    """
    entity model serializer
    """
    solution_id = serializers.IntegerField(required=True)
    fields = FieldSerializer(many=True)

    class Meta:
        model = Entity
        fields = ('id', 'name', 'solution_id', 'fields', )


class MapSerializer(serializers.ModelSerializer):
    app_id = serializers.IntegerField(required=True)

    class Meta:
        model = EntityMap
        fields = ('id', 'app_id', 'fields', )
