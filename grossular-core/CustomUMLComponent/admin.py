from django.contrib import admin
from CustomUMLComponent.models import GrossularCustomUMLComponent, GrossularCustomUMLComponentInterface, \
    GrossularCustomUMLComponentPackage, GrossularCustomUMLComponentRelationship

# Register your models here.


admin.site.register(GrossularCustomUMLComponentPackage)
admin.site.register(GrossularCustomUMLComponentRelationship)
admin.site.register(GrossularCustomUMLComponent)
admin.site.register(GrossularCustomUMLComponentInterface)
