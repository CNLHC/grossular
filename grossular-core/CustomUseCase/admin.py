from django.contrib import admin
from Project.models import GrossularProject
from CustomUseCase.models import GrossularCustomUseCase
from CustomUseCase.models import GrossularCustomUseCaseActor
from CustomUseCase.models import GrossularCustomUseCaseSubsystem
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


# Register your models here.

class ProjectFilter(SimpleListFilter):
    title = _('Project')  # or use _('country') for translated title
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        return tuple([(pro.codeName, pro.name) for pro in GrossularProject.objects.all()])

    def queryset(self, request, queryset):
        print(request)
        print(self.value())
        print(queryset)
        return queryset.filter(grossularProject__codeName=self.value())


class AdminGrossularCustomUseCase(admin.ModelAdmin):
    list_filter = (ProjectFilter,)


admin.site.register(GrossularCustomUseCase, AdminGrossularCustomUseCase)
admin.site.register(GrossularCustomUseCaseActor)

admin.site.register(GrossularCustomUseCaseSubsystem)
