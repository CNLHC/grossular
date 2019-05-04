from django.db import models
from Project.models import GrossularProject
from polymorphic.models import PolymorphicModel


class GrossularCustomElement(PolymorphicModel):
    grossularProject = models.ForeignKey(GrossularProject, on_delete=models.CASCADE,
                                         related_name='%(app_label)s_%(class)s_related')

    class Meta:
        abstract = True


class GrossularCustomUMLType(GrossularCustomElement):
    name = models.CharField(max_length=128)
    comment = models.TextField()
