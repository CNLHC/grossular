from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User,Group


class GrossularAdmin(AdminSite):
    site_title = _('Grossular')
    site_header = _('Grossular')
    index_title = _('Grossular Elements administration')




GrossularAdminSite = GrossularAdmin()
