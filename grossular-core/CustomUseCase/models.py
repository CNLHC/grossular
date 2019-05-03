from django.db import models
from CustomUMLBase.models import GrossularCustomElement
from CustomUseCase.manager import GrossularUseCaseManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class GrossularCustomUseCaseActor(GrossularCustomElement):
    name = models.CharField(max_length=40, unique=True)
    generalization = models.ForeignKey('CustomUseCase.GrossularCustomUseCaseActor', on_delete=models.SET_NULL,
                                       related_name="concrete", null=True, default=None, blank=True,
                                       verbose_name=_("generalization")
                                       )
    grossular = GrossularUseCaseManager()

    def __str__(self):
        return "{name}".format(name=self.name)

    class Meta:
        verbose_name = _("Actor")
        verbose_name_plural = _("Actors")


class GrossularCustomUseCaseSubsystem(GrossularCustomElement):
    name = models.CharField(max_length=100,
                            verbose_name=_("Subsystem Name")
                            )
    codeName = models.CharField(max_length=100, verbose_name=_("Subsystem code name")
                                )

    grossular = GrossularUseCaseManager()

    def save(self, *args, **kwargs):
        if GrossularCustomUseCaseSubsystem.objects.filter(grossularProject=self.grossularProject).filter(
                codeName=self.codeName).exclude(id=self.id).exists():
            raise ValidationError('Name must be unique per project')
        super(GrossularCustomUseCaseSubsystem, self).save(*args, **kwargs)

    def __str__(self):
        return "{name}".format(name=self.name)

    class Meta:
        verbose_name = _("Subsystem")
        verbose_name_plural = _("Subsystems")


class GrossularCustomUseCase(GrossularCustomElement):
    name = models.CharField(max_length=100, verbose_name=_("Case name"))
    comments = models.TextField(verbose_name=_("Case comments"))
    association = models.ManyToManyField(GrossularCustomUseCaseActor, blank=True, verbose_name=_("Case association"))

    include = models.ManyToManyField('CustomUseCase.GrossularCustomUseCase', blank=True, related_name="parent",
                                     verbose_name=_("Case include"))

    extend = models.ManyToManyField('CustomUseCase.GrossularCustomUseCase', blank=True, related_name="extension",
                                    verbose_name=_("Case extend"))
    generalization = models.ForeignKey('CustomUseCase.GrossularCustomUseCase', on_delete=models.SET_NULL,
                                       related_name="concrete", null=True, default=None, blank=True,
                                       verbose_name=_("Case generalization"))

    subsystem = models.ForeignKey('CustomUseCase.GrossularCustomUseCaseSubsystem', on_delete=models.CASCADE, null=True,
                                  default=None, related_name="useCases", blank=True, verbose_name=_("Subsystem"))
    grossular = GrossularUseCaseManager()

    def __str__(self):
        if self.subsystem is not None:
            return "{subsystem}-{name}".format(name=self.name, subsystem=self.subsystem.name)
        else:
            return "{name}".format(name=self.name)

    class Meta:
        verbose_name = _("UML Case")
        verbose_name_plural = _("UML Cases")
