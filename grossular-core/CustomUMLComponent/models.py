from django.db import models
from CustomUMLBase.models import GrossularCustomElement
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class GrossularCustomUMLComponent(GrossularCustomElement):
    name = models.CharField(max_length=128, verbose_name=_("Component Name"))
    codeName = models.CharField(max_length=128, verbose_name=_("Component Code Name"))
    package = models.ForeignKey('CustomUMLComponent.GrossularCustomUMLComponentPackage', related_name="components",
                                null=True, on_delete=models.SET_NULL, default=None, verbose_name=(_("package")))

    class Meta:
        verbose_name = _("Component")
        verbose_name_plural = _("Components")

    def __str__(self):
        if self.package is None:
            return "{0}({1})".format(self.name, self.codeName)
        else:
            return "{pn}-{n}({cn})".format(pn=self.package.name, n=self.name, cn=self.codeName)


class GrossularCustomUMLComponentInterface(GrossularCustomElement):
    name = models.CharField(max_length=128, verbose_name=_("Interface Name"))
    Component = models.ForeignKey('CustomUMLComponent.GrossularCustomUMLComponent', on_delete=models.CASCADE,
                                  related_name='interfaces', verbose_name=_("Component"))

    class Meta:
        verbose_name = _("Interface")
        verbose_name_plural = _("Interfaces")

    def __str__(self):
        return  "{0}-{1}".format(self.Component.__str__(),self.name)


class GrossularCustomUMLComponentRelationship(GrossularCustomElement):
    invoker = models.ForeignKey('CustomUMLComponent.GrossularCustomUMLComponent', on_delete=models.CASCADE,
                                related_name="using", verbose_name=_("Invoker"))

    interface = models.ForeignKey('CustomUMLComponent.GrossularCustomUMLComponentInterface', on_delete=models.CASCADE,
                                  related_name="connection", verbose_name=_("Interface"))

    class Meta:
        verbose_name = _("Invoke relationship")
        verbose_name_plural = _("Invoke Relationships")

    def __str__(self):
        return "{invoker} --> {interface}({id})".format(invoker=self.invoker.name,interface=self.interface.name,id=self.interface.id)






class GrossularCustomUMLComponentPackage(GrossularCustomElement):
    PACKAGE_SHAPE_CHOICES = (
        ("package", _("package")),
        ("node", _("node")),
        ("cloud", _("cloud")),
        ("database", _("database")),
    )
    name = models.CharField(max_length=128, verbose_name=_("Package name"))
    shape = models.CharField(max_length=20, choices=PACKAGE_SHAPE_CHOICES, verbose_name=_("Package Shape"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Component Package")
        verbose_name_plural = _("Component Packages")
