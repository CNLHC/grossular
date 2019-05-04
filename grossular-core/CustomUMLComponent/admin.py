from django.contrib import admin
from grossular.admin import GrossularAdminSite
from Project.models import GrossularProject
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from CustomUMLComponent.models import GrossularCustomUMLComponent, GrossularCustomUMLComponentInterface, \
    GrossularCustomUMLComponentPackage, GrossularCustomUMLComponentRelationship

from CustomUMLBase.adminUtil import GrossularProjectFilter


# Register your models here.

class PackageFilter(SimpleListFilter):
    title = _('Subsystem')
    parameter_name = 'subsystem'

    def lookups(self, request, model_admin):
        projectCodeName = request.GET.get('project')
        return tuple([(j.name, j.name) for j in
                      GrossularCustomUMLComponentPackage.objects.all().filter(grossularProject__codeName=projectCodeName)])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(package__name=self.value())


class AdminGrossularCustomComponent(admin.ModelAdmin):
    list_filter = (GrossularProjectFilter, PackageFilter)


GrossularAdminSite.register(GrossularCustomUMLComponent, AdminGrossularCustomComponent)
GrossularAdminSite.register(GrossularCustomUMLComponentPackage)
GrossularAdminSite.register(GrossularCustomUMLComponentRelationship)
GrossularAdminSite.register(GrossularCustomUMLComponentInterface)
