from django.db import models


# Create your models here.


class GrossularClass(models.Model):
    PRO_MODIFIER = (
    )

    Name = models.TextField()
    IsAbstract = models.BooleanField(default=False)
    IsInterface = models.BooleanField(default=False)
    Brief = models.CharField(max_length=200)
    Notes = models.TextField(blank=True,default='')



class GrossularClassMember(models.Model):
    VIS_MODIFIER = (
        ('+', 'public'),
        ('~', 'package'),
        ('#', 'protected'),
        ('-', 'private')
    )
    Class = models.ForeignKey(GrossularClass)
    Name  = models.CharField(max_length=128)
    VisibilityModifier = models.CharField(max_length=5, choices=VIS_MODIFIER)


class GrossularType(models.Model):
    pass


