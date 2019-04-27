from django.db import models


class GrossularUseCaseManager(models.Manager):
    def get_queryset(self):
        return  super().get_queryset().all()

    def inProject(self,projectName:str):
        return self.get_queryset().filter(grossularProject__codeName=projectName)

