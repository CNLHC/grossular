from django.db import models

# Create your models here.

class GrossularProject(models.Model):
    name = models.TextField()
    codeName = models.CharField(max_length=40,unique=True)
    customer = models.CharField(max_length=100)
    def  __str__(self):
        return "{codeName}-{name}".format(codeName=self.codeName,name  = self.name)

