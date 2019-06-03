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

    def build_table_name(self):
        solution = models.Solution.objects.get(pk=self.validated_data['solution_id'])
        solution_name = solution.name[0:30].strip().lower()
        entity_name = self.validated_data['name'][0:30].strip().lower()
        return f'{solution_name}_{entity_name}'

    def create(self, validated_data):
        validated_data['table'] = self.build_table_name()
        return super(WritableNestedModelSerializer, self).create(validated_data)

    def save(self, **kwargs):
        instance = super(WritableNestedModelSerializer, self).save(**kwargs)
        migration = instance.make_migration()

        if migration:
            migration.run()

        return instance


class MappedFieldSerializer(serializers.ModelSerializer):
    field_id = serializers.IntegerField(required=True)
    field = serializers.SlugRelatedField(slug_field='field_type', read_only=True)
    entity_map_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.MappedField
        fields = ('id', 'field_id', 'field', 'alias', 'entity_map_id', )


class EntityMapSerializer(WritableNestedModelSerializer):
    app_id = serializers.IntegerField(required=True)
    entity_id = serializers.IntegerField(required=True)
    fields = MappedFieldSerializer(many=True)

    class Meta:
        model = models.EntityMap
        fields = ('id', 'app_id', 'entity_id', 'name', 'fields', )

        validators = [
            UniqueTogetherValidator(
                queryset=models.EntityMap.objects.all(),
                fields=('entity_id', 'name'))
        ]
