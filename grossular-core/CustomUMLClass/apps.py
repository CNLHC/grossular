from django.apps import AppConfig
from  django.utils.translation import ugettext_lazy as _

class CustomUmlClassConfig(AppConfig):
    name = 'CustomUMLClass'
    verbose_name = _('UML Class')



