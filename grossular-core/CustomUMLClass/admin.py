from django.contrib import admin
from CustomUMLClass.models import GrossularCustomUMLClass,GrossularCustomUMLClassMethod,GrossularCustomUMLClassRelationship

# Register your models here.

admin.site.register(GrossularCustomUMLClass)
admin.site.register(GrossularCustomUMLClassMethod)
admin.site.register(GrossularCustomUMLClassRelationship)