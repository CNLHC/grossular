from django.db import models
from polymorphic.models import PolymorphicModel
import enum


# Create your models here.

class GrossularStdElement(PolymorphicModel):
    """
ref to :cite:`UML251` ,7.2.3.1 ,Page 64

An Element is a constituent of a model. Descendants of Element provide semantics appropriate to the concept they
represent.

Every Element has the inherent capability of owning other Elements. When an Element is removed from a model, all its
ownedElements are also necessarily removed from the model. The abstract syntax for each kind of Element specifies
what other kind of Elements it may own. Every Element in a model must be owned by exactly one other Element of that
model, with the exception of the top-level Packages of the model
    """
    IDElement=models.IntegerField(primary_key=True)



class GrossularStdComments(GrossularStdElement):
    """
ref to :cite:`UML251` ,7.2.3.2 ,Page 64

Every kind of Element may own Comments. The ownedComments for an Element add no semantics but may represent
information useful to the reader of the model.
    """
    owningElement = models.ForeignKey(GrossularStdElement, related_name="ownedElement",on_delete=models.CASCADE)
    body = models.TextField(blank=True)


class GrossularStdRelationship(GrossularStdElement):
    """
ref to :cite:`UML251` ,7.2.3.3 ,Page 64

A Relationship is an Element that specifies some kind of relationship between other Elements. Descendants of
Relationship provide semantics appropriate to the concept they represent.
    """
    RelationShipToParent = models.OneToOneField(GrossularStdElement, parent_link=True,on_delete=models.CASCADE)



class GrossularStdDirectedRelationship(GrossularStdRelationship):
    """
ref to :cite:`UML251` ,7.2.3.3 ,Page 64

A DirectedRelationship represents a Relationship between a collection of source model elements and a collection of
target model elements. A DirectedRelationship is said to be directed from the source elements to the target elements.
    """
    DirectedRelationShipToParent = models.OneToOneField(GrossularStdRelationship, parent_link=True,on_delete=models.CASCADE)
    IDDirectedRelationship=models.IntegerField(primary_key=True)



class GrossularStdEnmuVisibilityKind(enum.Enum):
    public = "public"
    private = "private"
    protected = "protected"
    package = "package"


class GrossularStdNamedElement(GrossularStdElement):
    """
ref to :cite:`UML251` ,7.4.3.2

    A NamedElement is an Element in a model that may have a name. The name may be used for identification of the
NamedElement within Namespaces where its name is accessible.
    """

    visibility_choices = (
        (GrossularStdEnmuVisibilityKind.public, GrossularStdEnmuVisibilityKind.public),
        (GrossularStdEnmuVisibilityKind.private, GrossularStdEnmuVisibilityKind.private),
        (GrossularStdEnmuVisibilityKind.protected, GrossularStdEnmuVisibilityKind.protected),
        (GrossularStdEnmuVisibilityKind.package, GrossularStdEnmuVisibilityKind.package))

    name = models.TextField(blank=True)
    qualifiedName = models.TextField(blank=True)
    visibility = models.CharField(max_length=20,choices=visibility_choices)



class GrossularStdNamespaces(GrossularStdNamedElement):
    """
ref to :cite:`UML251` ,7.4.3.1

A Namespace provides a container for NamedElements, which are called its ownedMembers. A Namespace may also
import NamedElements from other Namespaces, in which case these, along with the ownedMembers, are members of the
importing Namespace
    """

    memberNamespace = models.ManyToManyField(GrossularStdNamedElement,related_name="ownedMember")

class GrossularStdPackageableElement(GrossularStdNamedElement):
    """
ref to :cite:`UML251` ,7.4.3.3

A PackageableElement is a NamedElement that may be owned directly by a Package (see Clause 12 on Packages). Any
such element may serve as a TemplateParameter (see sub clause 7.3 on Templates).
    """
    IDPackageableElement = models.IntegerField(primary_key=True)


#TODO : 7.4.3.3 Package


class GrossularStdType(GrossularStdPackageableElement):
    """
ref to :cite:`UML251` ,7.5.3.1

A Type specifies a set of allowed values known as the instances of the Type. Depending on the kind of Type, instances
of the Type may be created or destroyed over time. However, the rules for what constitutes an instance of the Type
remain fixed by the definition of that Type. All Types in UML are Classifiers (see Clause 9).
    """




class GrossularStdTypedElement(GrossularStdNamedElement):
    """
ref to :cite:`UML251` ,7.5.3.1

A TypedElement is a NamedElement that, in some way, represents particular values. Depending on the kind of
TypedElement, the actual values that it represents may change over time. Examples of kinds of TypedElement include
ValueSpecification, which directly specifies a collection of values (see Clause 8), and StructuralFeature, which
represents values held as part of the structure of the instances of the Classifier that owns it (see sub clause 9.4).
    """
    type = models.ForeignKey(GrossularStdType,null=True,on_delete=models.SET_DEFAULT,related_name="typedElement",default=None)



class GrossularStdMultiplicityElement(GrossularStdElement):
    """
ref to :cite:`UML251` ,7.5.3.2


    A MultiplicityElement is an Element that may be instantiated in some way to represent a collection of values.
Depending on the kind of MultiplicityElement, the values in the collection may change over time. Examples of kinds of
MultiplicityElement include StructuralFeature, which has values in the context of an instance of the Classifier that owns
it (see sub clause 9.4) and Variable, which has values in the context of the execution of an Activity (see sub clause 15.2

    """
    isOrdered = models.BooleanField(default=False)
    isUnique = models.BooleanField(default=True)
    #TODO: add Upper and lower bound
    #TODO: add manager to generate standard muliplicityElement


class GrossularStdConstraint(GrossularStdPackageableElement):
    #TODO: add imple
    pass


class GrossularStdDependency(GrossularStdDirectedRelationship,GrossularStdPackageableElement):
    supplier = models.ManyToManyField(GrossularStdNamedElement,related_name="supplierDependency")


class GrossularStdAbstraction(GrossularStdDependency):
    pass

class GrossularStdRealization(GrossularStdAbstraction):
    pass

class GrossularStdUsage(GrossularStdDependency):
    pass







