from django.db import models
from CustomUMLBase.models import GrossularCustomElement, GrossularCustomUMLType
from django.utils.translation import gettext as _


# Create your models here.
class GrossularCustomUMLClass(GrossularCustomUMLType):
    # @override
    # name = models.CharField(max_length=128)
    # @override
    # comment = models.TextField()

    SPECIFICATION_CHOICES = (
        ('normal', _('normal')),
        ('abstract', _('abstract')),
        ('interface', _('interface'))
    )
    specification = models.CharField(max_length=20, choices=SPECIFICATION_CHOICES, default='normal')
    component = models.ForeignKey("CustomUMLComponent.GrossularCustomUMLComponent", null=True, default=None,
                                  on_delete=models.SET_NULL, related_name="classes", verbose_name=_("components"))

    def __str__(self):
        if self.component is None:
            return "{name}".format(name=self.name)
        else:
            return "{comp}-{name}".format(comp=self.component.name, name=self.name)

    class Meta:
        verbose_name = _("Class")
        verbose_name_plural = _("Classes")


class GrossularCustomUMLClassRelationship(GrossularCustomElement):
    CLASS_RELATIONSHIP_TYPE_CHOICES = (
        ('inheritance', _('inheritance')),
        ('generalizations', _('generalizations')),
        ('composition ', _('composition')),
        ('aggregations', _('aggregations')),
        ('associations ', _('associations')),
        ('dependencies', _('dependencies'))
    )

    type = models.CharField(max_length=20, choices=CLASS_RELATIONSHIP_TYPE_CHOICES, verbose_name=_("relation name"))

    left = models.ForeignKey('CustomUMLClass.GrossularCustomUMLClass', on_delete=models.SET_NULL, null=True,
                             default=None, related_name="RelationshipAsLeft", verbose_name=_("relation from"))

    right = models.ForeignKey('CustomUMLClass.GrossularCustomUMLClass', on_delete=models.SET_NULL, null=True,
                              default=None,
                              related_name="RelationshipAsRight", verbose_name=_("relation to"))

    leftLabel = models.CharField(max_length=20, blank=True, default='', verbose_name=_("from side label"))

    rightLabel = models.CharField(max_length=20, blank=True, default='', verbose_name=_("to side label"))

    def __str__(self):
        return "{cl}-{relation}-{cr}".format(cl=self.left.name, cr=self.right.name, relation=self.type)

    class Meta:
        verbose_name = _("Class Relationship")
        verbose_name_plural = _("Classes Relationships")


class GrossularCustomUMLClassElement(GrossularCustomElement):
    VISIBILITY_CHOICES = (
        ('public', _('public')),
        ('protected', _('protected')),
        ('private', _('private')),
        ('package', _('package')),
    )
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, verbose_name=("Method visibility"))

    master = models.ForeignKey('CustomUMLClass.GrossularCustomUMLClass', on_delete=models.CASCADE, null=True,
                               default=None, related_name="element_%(class)s", verbose_name=_("Class"))
    name = models.CharField(max_length=128, verbose_name=_("Element name"))

    comment = models.TextField(verbose_name=_("Element Comment"))

    type = models.ForeignKey('CustomUMLBase.GrossularCustomUMLType', on_delete=models.SET_NULL, null=True, default=None,
                             related_name="typed_%(class)s",
                             verbose_name=_("Element type"))

    class Meta:
        abstract = True


class GrossularCustomUMLClassMethod(GrossularCustomUMLClassElement):

    def __str__(self):
        return "{cn}-{mn}".format(cn=self.master.name, mn=self.name)

    class Meta:
        verbose_name = _("Class Method")
        verbose_name_plural = _("Classes Methods")


class GrossularCustomUMLClassMember(GrossularCustomUMLClassElement):

    def __str__(self):
        return "{cn}-{mn}".format(cn=self.master.name, mn=self.name)

    class Meta:
        verbose_name = _("Class Member")
        verbose_name_plural = _("Classes Members")
