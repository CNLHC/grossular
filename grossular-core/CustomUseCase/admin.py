from django.contrib import admin
from CustomUseCase.models import GrossularCustomUseCase
from CustomUseCase.models import GrossularCustomUseCaseActor
from CustomUseCase.models import GrossularCustomUseCaseSubsystem

# Register your models here.

admin.site.register(GrossularCustomUseCase)
admin.site.register(GrossularCustomUseCaseActor)
admin.site.register(GrossularCustomUseCaseSubsystem)
