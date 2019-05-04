from django.contrib import admin
from Project.models import GrossularProject
from grossular.admin import  GrossularAdminSite

# Register your models here.


GrossularAdminSite.register(GrossularProject)
