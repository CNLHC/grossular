from django.apps import AppConfig
from  django.utils.translation import ugettext_lazy as _


class CustomUmlCaseConfig(AppConfig):
    name = 'CustomUseCase'
    verbose_name = _("Case")





