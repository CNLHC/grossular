about this django-app
=======================

This app was  called `StdUML` since we want to represent **standard** uml model. 
for example, to represent an UML `class`, instead of creating a new `django.models.Model` class and add some fields into
it, we will create  new (model) class inherit from  `EncapsulatedClassifier` and `BehavioredClassifier` just like  what "Unified Modeling Language"
document describe.

We believe that this app can be develop in a higher abstract level instead of reading the doc and translating its' conception into python code.  This is because
OMG®( who design and publish UML standards) also provides machine readable XML file to describe what `element`(it seems that `element`
 was a special term in  UML standards, all other UML objects were designed to derive from `element`) standard UML have and
the releationship between `elements`.

Generating all django model from machine readable XML file was awesome since once generated code can work properly

1. it is highly probably that it totally meet the UML standards.
2. we can keep on track with newer version of UML standards with no pain(if OMG® does not change the meta-info format)

To achieve that goal, We must define django ORM model equivalence of UML meta-info. for example, an `element`  can have relationship to any number of
`Comment`  objects, this was  depicted by follow XML snippets

```

<ownedAttribute xmi:type="uml:Property" xmi:id="Element-ownedComment" name="ownedComment"
               aggregation="composite" type="Comment"
               association="A_ownedComment_owningElement">
  <subsettedProperty xmi:idref="Element-ownedElement"/>
  <ownedComment xmi:type="uml:Comment" xmi:id="Element-ownedComment-_ownedComment.0"
                body="The Comments owned by this Element.">
     <annotatedElement xmi:idref="Element-ownedComment"/>
  </ownedComment>
  <lowerValue xmi:type="uml:LiteralInteger" xmi:id="Element-ownedComment-_lowerValue"/>
  <upperValue xmi:type="uml:LiteralUnlimitedNatural"
              xmi:id="Element-ownedComment-_upperValue"
              value="*"/>
</ownedAttribute>

```

1. from `ownedAttribute` tag attribute, we know `Comment` `Composite` `Element`

we can add `models.Foreignkey` to `Comment` model and due to the properties of `Composite` relationship, the foreignkey must
be set to `null=false` since  `Comment` object can not exist without an `element` object.

Adding `models.ManyToManyField` to represent same thing seems available too because so far we do not know if it is legal to use one
`Comment` object to comment multiple `Element` objects. (same thing happen to 1 `Element` and multiple `Comment`)


2. from `lowerValue` and `upperValue`, we can know that one `Element` can have any number of `Comment`

`lowerValue ` was LiteralInteger and 0 was obviously in it.  `upperView`  was `LiteralUnlimitedNatural` and infinite was obviously in it.
so we discard `models.Foreignkey` and choose `models.ManyToManyField`.


with these two info, we can use django model class like

```

class GrossularStdElement(models.Model):
    IDElement=models.IntegerField(primary_key=True)
    ownedElement= models.ForeignKey('StdUML.GrossularStdComments', related_name="owningElement",on_delete=models.CASCADE)

```











