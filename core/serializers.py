from rest_framework import serializers

from drf_writable_nested import WritableNestedModelSerializer

from core import models
from core import queue
from external import migration


class SolutionSerializer(serializers.ModelSerializer):
    """
    solution model serializer
    """
    class Meta:
        model = models.Solution
        fields = ('id', 'name',)


class AppSerializer(serializers.ModelSerializer):
    """
    app model serializer
    """
    solution_id = serializers.IntegerField(required=True)

    class Meta:
        model = models.App
        fields = ('id', 'name', 'solution_id', )


class FieldSerializer(serializers.ModelSerializer):
    """
    entity model serializer
    """
    field_type = serializers.CharField()

    class Meta:
        model = models.Field
        fields = ('pk', 'name', 'field_type',)


class EntitySerializer(WritableNestedModelSerializer):
    """
    entity model serializer
    """
    solution_id = serializers.IntegerField(required=True)
    fields = FieldSerializer(many=True)

    class Meta:
        model = models.Entity
        fields = ('id', 'name', 'solution_id', 'fields', )

    def save(self, **kwargs):
        return super(EntitySerializer, self).save(
            migration=models.Migration.objects.create(),
            **kwargs)


class MappedFieldSerializer(serializers.ModelSerializer):
    field_id = serializers.IntegerField(required=True)
    field = serializers.SlugRelatedField(slug_field='field_type', read_only=True)

    class Meta:
        model = models.MappedField
        fields = ('id', 'field_id', 'field', 'alias', )


class EntityMapSerializer(WritableNestedModelSerializer):
    app_id = serializers.IntegerField(required=True)
    entity_id = serializers.IntegerField(required=True)
    fields = MappedFieldSerializer(many=True)

    class Meta:
        model = models.EntityMap
        fields = ('id', 'app_id', 'entity_id', 'name', 'fields', )

