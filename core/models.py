from django.db import models


class Solution(models.Model):
    """
    Solution model. This is the main solution to which the platform will serve. (SAGER)
    """
    name = models.CharField(max_length=30)


class Entity(models.Model):
    """
    Entity model. This is the Entity that will be used in the solution. (USINA)
    """
    name = models.CharField(max_length=30)
    solution = models.ForeignKey(Solution, on_delete=None)


class App(models.Model):
    """
    app model
    """
    name = models.CharField(max_length=30)
    solution = models.ForeignKey(Solution, on_delete=None)


class Field(models.Model):
    """
    field model
    """
    name = models.CharField(max_length=30)
    typeName = models.CharField(max_length=30)
    entity = models.ForeignKey(Entity, on_delete=None)














