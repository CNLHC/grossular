from django.db import models
from CustomUMLBase.models import  GrossularCustomElement
from CustomUseCase.manager import GrossularUseCaseManager
from django.core.exceptions import ValidationError


# Create your models here.

class GrossularCustomUseCaseActor(GrossularCustomElement):
    name = models.CharField(max_length=40,unique=True)
    generalization = models.ForeignKey('CustomUseCase.GrossularCustomUseCaseActor', on_delete=models.SET_NULL,related_name="concrete",null=True,default=None,blank=True)
    grossular =  GrossularUseCaseManager()

    def __str__(self):
        return "{name}".format(name=self.name)

class GrossularCustomUseCaseSubsystem(GrossularCustomElement):
    name = models.CharField(max_length=100)
    codeName = models.CharField(max_length=100)
    grossular =  GrossularUseCaseManager()

    def save(self, *args, **kwargs):
        if GrossularCustomUseCaseSubsystem.objects.filter(grossularProject=self.grossularProject).filter(codeName=self.codeName).exclude(id=self.id).exists():
            raise  ValidationError('Name must be unique per project')
        super(GrossularCustomUseCaseSubsystem, self).save(*args, **kwargs)

    def __str__(self):
        return "{name}".format(name=self.name)


class GrossularCustomUseCase(GrossularCustomElement):
    name = models.CharField(max_length=100)
    comments = models.TextField()
    association = models.ManyToManyField(GrossularCustomUseCaseActor,blank=True)
    include = models.ManyToManyField('CustomUseCase.GrossularCustomUseCase',blank=True,related_name="parent")
    extend = models.ManyToManyField('CustomUseCase.GrossularCustomUseCase',blank=True,related_name="extension")
    generalization = models.ForeignKey('CustomUseCase.GrossularCustomUseCase', on_delete=models.SET_NULL,related_name="concrete",null=True,default=None,blank=True)
    subsystem = models.ForeignKey('CustomUseCase.GrossularCustomUseCaseSubsystem', on_delete=models.CASCADE,null=True,default=None,related_name="useCases",blank=True)
    grossular =  GrossularUseCaseManager()

    def __str__(self):
        return "{name}".format(name=self.name)



