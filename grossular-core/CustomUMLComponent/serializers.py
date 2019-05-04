from rest_framework import serializers
from .models import GrossularCustomUMLComponent, GrossularCustomUMLComponentRelationship, \
    GrossularCustomUMLComponentInterface, GrossularCustomUMLComponentPackage


class GrossularCustomUMLComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrossularCustomUMLComponent
        fields = "__all__"


class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrossularCustomUMLComponentInterface
        fields = "__all__"


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrossularCustomUMLComponentRelationship
        fields = ('interface',)


class ComponentDetailSerializer(serializers.ModelSerializer):
    using = RelationshipSerializer(many=True)
    interfaces = InterfaceSerializer(many=True)

    class Meta:
        model = GrossularCustomUMLComponent
        fields = "__all__"
