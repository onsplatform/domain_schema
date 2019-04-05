from django.db import models


class Solution(models.Model):
    """
    solution model
    """
    name = models.CharField(max_length=30)


class EntityModel(models.Model):
    """
    entity model
    """
    name = models.CharField(max_length=30)
    solution = models.ForeignKey(Solution, on_delete=None)
