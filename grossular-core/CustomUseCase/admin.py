from Project.models import GrossularProject
from CustomUseCase.models import GrossularCustomUseCase
from CustomUseCase.models import GrossularCustomUseCaseActor
from CustomUseCase.models import GrossularCustomUseCaseSubsystem
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from grossular.admin import GrossularAdminSite
from django.contrib import  admin


# Register your models here.

class ProjectFilter(SimpleListFilter):
    title = _('Project')
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        return tuple([(pro.codeName, pro.name) for pro in GrossularProject.objects.all()])

    def queryset(self, request, queryset):
        return queryset.filter(grossularProject__codeName=self.value())


class SubsystemFilter(SimpleListFilter):
    title = _('Subsystem')
    parameter_name = 'subsystem'

    def lookups(self, request, model_admin):
        projectCodeName = request.GET.get('project')
        return tuple([(sys.codeName, sys.name) for sys in GrossularCustomUseCaseSubsystem.objects.all().filter(grossularProject__codeName=projectCodeName)])

    def queryset(self, request, queryset):
        return queryset.filter(subsystem__codeName=self.value())


class AdminGrossularCustomUseCase(admin.ModelAdmin):
    list_filter = (ProjectFilter, SubsystemFilter)


GrossularAdminSite.register(GrossularCustomUseCase, AdminGrossularCustomUseCase)
GrossularAdminSite.register(GrossularCustomUseCaseActor)
GrossularAdminSite.register(GrossularCustomUseCaseSubsystem)
