from django.contrib.admin import SimpleListFilter
from Project.models import GrossularProject
from django.utils.translation import ugettext_lazy as _

class GrossularProjectFilter(SimpleListFilter):
    title = _('Project')
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        return tuple([(pro.codeName, pro.name) for pro in GrossularProject.objects.all()])

    def queryset(self, request, queryset):
        return queryset.filter(grossularProject__codeName=self.value())
