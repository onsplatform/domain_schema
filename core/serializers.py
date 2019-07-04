from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from drf_writable_nested import WritableNestedModelSerializer

from core import models, queue
from external import migration


class SolutionSerializer(serializers.ModelSerializer):
    """
    solution model serializer
    """
    name = serializers.CharField(
        validators=[
            UniqueValidator(queryset=models.Solution.objects.all())
        ]
    )

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
        validators = [
            UniqueTogetherValidator(
                queryset=models.App.objects.all(),
                fields=('solution_id', 'name'))
        ]


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
    fields = FieldSerializer(many=True, required=False)
    table = serializers.CharField(read_only=True)

    class Meta:
        model = models.Entity
        fields = ('id', 'solution_id', 'name', 'fields', 'table',  )
        validators = [
            UniqueTogetherValidator(
                queryset=models.Entity.objects.all(),
                fields=('solution_id', 'name'))
        ]

    def save(self, **kwargs):
        instance = super(WritableNestedModelSerializer, self).save(**kwargs)
        migration = instance.make_migration()

        if migration:
            migration.run()

        return instance


class MapFilterParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MapFilterParameter
        fields = ('name', 'is_array', )
        validators = [
            UniqueTogetherValidator(
                queryset=models.MapFilterParameter.objects.all(),
                fields=('filter_id', 'name', ))
        ]


class MapFilterSerializer(serializers.ModelSerializer):
    parameters = MapFilterParameterSerializer(many=True)

    class Meta:
        model = models.MapFilter
        fields = ('name', 'expression', 'parameters', )
        validators = [
            UniqueTogetherValidator(
                queryset=models.MapFilter.objects.all(),
                fields=('map_id', 'name'))
        ]


class MappedFieldSerializer(serializers.ModelSerializer):
    field_id = serializers.IntegerField(required=True, write_only=True)
    field_type = serializers.ReadOnlyField(source='field.field_type', read_only=True)
    column_name = serializers.ReadOnlyField(source='field.name', read_only=True)

    class Meta:
        model = models.MappedField
        fields = ('field_id', 'field_type', 'column_name', 'alias', )


class EntityMapSerializer(WritableNestedModelSerializer):
    class EntityNestedSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Entity
            fields = ('name', 'table',)

   # app_id = serializers.IntegerField(required=True, write_only=True)
    app_id = serializers.IntegerField(required=True)
    entity_id = serializers.IntegerField(required=True, write_only=True)
    fields = MappedFieldSerializer(many=True)
    filters = MapFilterSerializer(many=True, required=False)
    model = EntityNestedSerializer(source='entity', read_only=True)

    class Meta:
        model = models.EntityMap
        fields = ('id', 'name', 'app_id', 'entity_id', 'model', 'fields', 'filters', )

        validators = [
            UniqueTogetherValidator(
                queryset=models.EntityMap.objects.all(),
                fields=('entity_id', 'name'))
        ]
