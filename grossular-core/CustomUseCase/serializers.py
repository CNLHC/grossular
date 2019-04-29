from rest_framework.serializers import ModelSerializer
from CustomUseCase.models import *

class CustomUseCaseSerializer(ModelSerializer):
    class Meta:
        model = GrossularCustomUseCase
        fields = ("__all__")

class CustomUseCaseDetailSerializer(ModelSerializer):
    concrete = CustomUseCaseSerializer(many=True)
    extension = CustomUseCaseSerializer(many=True)
    include  = CustomUseCaseSerializer(many=True)
    extend = CustomUseCaseSerializer(many=True)

    class Meta:
        model = GrossularCustomUseCase
        fields = ("__all__")


class CustomUseCaseActorSerializer(ModelSerializer):
    class Meta:
        model =  GrossularCustomUseCaseActor
        fields = "__all__"

class CustomUseCaseSubsystemSerializer(ModelSerializer):
    class Meta:
        model =   GrossularCustomUseCaseSubsystem
        fields = "__all__"

