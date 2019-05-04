from Project.models import GrossularProject
from CustomUseCase.models import GrossularCustomUseCase
from CustomUseCase.models import GrossularCustomUseCaseActor
from CustomUseCase.models import GrossularCustomUseCaseSubsystem
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from grossular.admin import GrossularAdminSite
from CustomUMLBase.adminUtil import GrossularProjectFilter
from django.contrib import  admin


# Register your models here.



class SubsystemFilter(SimpleListFilter):
    title = _('Subsystem')
    parameter_name = 'subsystem'

    def lookups(self, request, model_admin):
        projectCodeName = request.GET.get('project')
        return tuple([(sys.codeName, sys.name) for sys in GrossularCustomUseCaseSubsystem.objects.all().filter(grossularProject__codeName=projectCodeName)])

    def queryset(self, request, queryset):
        return queryset.filter(subsystem__codeName=self.value())


class AdminGrossularCustomUseCase(admin.ModelAdmin):
    list_filter = (GrossularProjectFilter, SubsystemFilter)

GrossularAdminSite.register(GrossularCustomUseCase, AdminGrossularCustomUseCase)
GrossularAdminSite.register(GrossularCustomUseCaseActor)
GrossularAdminSite.register(GrossularCustomUseCaseSubsystem)
