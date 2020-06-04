from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from drf_writable_nested import WritableNestedModelSerializer

from core import models
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
        fields = ('id', 'name', 'description', 'is_reprocessing', 'is_reprocessable',)


class BranchSerializer(serializers.ModelSerializer):
    """
    branch model serializer
    """
    name = serializers.CharField(required=True)
    solution_id = serializers.IntegerField(required=True)

    class Meta:
        model = models.Branch
        fields = ('id', 'name', 'solution_id', 'created_at', 'deleted', 'description',
                  'meta_instance_id', 'modified', 'owner', 'started_at', 'status')


class ReprocessSerializer(serializers.ModelSerializer):
    """
    reprocess model serializer
    """

    class Meta:
        model = models.Reprocess
        fields = ('id', 'solution_id', 'tag', 'reprocess_instance_id', 'date_created',
                  'modified', 'is_reprocessing')


class ReproductionSerializer(serializers.ModelSerializer):
    """
    reproduction model serializer
    """

    class Meta:
        model = models.Reprocess
        fields = ('id', 'solution_id', 'tag', 'reproduction_instance_id', 'date_created',
                  'modified', 'is_reproducing')


class AppSerializer(serializers.ModelSerializer):
    """
    app model serializer
    """
    solution_id = serializers.IntegerField(required=True)

    class Meta:
        model = models.App
        fields = ('id', 'name', 'solution_id', 'container', 'type', 'technology')
        validators = [
            UniqueTogetherValidator(
                queryset=models.App.objects.all(),
                fields=('solution_id', 'name'))
        ]


class AppVersionSerializer(serializers.ModelSerializer):
    """
    app version model serializer
    """
    app_id = serializers.IntegerField(required=True)

    class Meta:
        model = models.AppVersion
        fields = ('id', 'app_id', 'version', 'tag', 'date_begin_validity', 'date_end_validity', 'process_id')
        validators = [
            UniqueTogetherValidator(
                queryset=models.AppVersion.objects.all(),
                fields=('app_id', 'version'))
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
        fields = ('id', 'solution_id', 'name', 'fields', 'table',)
        validators = [
            UniqueTogetherValidator(
                queryset=models.Entity.objects.all(),
                fields=('solution_id', 'name'))
        ]

    def save(self, **kwargs):
        # __import__('ipdb').set_trace()
        instance = super(WritableNestedModelSerializer, self).save(**kwargs)
        migration = instance.make_migration()

        if migration:
            migration.run()

        return instance


class MapFilterParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MapFilterParameter
        fields = ('name', 'is_array',)
        validators = [
            UniqueTogetherValidator(
                queryset=models.MapFilterParameter.objects.all(),
                fields=('filter_id', 'name',))
        ]


class MapFilterSerializer(serializers.ModelSerializer):
    parameters = MapFilterParameterSerializer(many=True)

    class Meta:
        model = models.MapFilter
        fields = ('name', 'expression', 'parameters',)
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
        fields = ('field_id', 'field_type', 'column_name', 'alias',)


class EntityMapSerializer(WritableNestedModelSerializer):
    class EntityNestedSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Entity
            fields = ('name', 'table', 'solution_id')

    def get_metadata(self, obj):
        return [
            {'field_type': str(models.FIELD_TYPES.BOOLEAN), 'column_name': 'deleted', 'alias': 'deleted'},
            {'field_type': str(models.FIELD_TYPES.VARCHAR), 'column_name': 'meta_instance_id', 'alias': 'instance_id'},
            {'field_type': str(models.FIELD_TYPES.DATE), 'column_name': 'modified', 'alias': 'modified_at'},
            {'field_type': str(models.FIELD_TYPES.DATE), 'column_name': 'date_created', 'alias': 'created_at'},
            {'field_type': str(models.FIELD_TYPES.VARCHAR), 'column_name': 'from_id', 'alias': 'from_id'},
            {'field_type': str(models.FIELD_TYPES.VARCHAR), 'column_name': 'branch', 'alias': 'branch'}
        ]

    app_version = AppVersionSerializer(required=True)
    entity_id = serializers.IntegerField(required=True, write_only=True)
    fields = MappedFieldSerializer(many=True)
    metadata = SerializerMethodField()
    filters = MapFilterSerializer(many=True, required=False)
    model = EntityNestedSerializer(source='entity', read_only=True)

    class Meta:
        model = models.EntityMap
        fields = ('id', 'name', 'app_version', 'entity_id', 'model', 'fields', 'metadata', 'filters',)

        validators = [
            UniqueTogetherValidator(
                queryset=models.EntityMap.objects.all(),
                fields=('entity_id', 'name'))
        ]
