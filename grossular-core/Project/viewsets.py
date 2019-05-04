from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from CustomUseCase.models import GrossularCustomUseCase, GrossularCustomUseCaseSubsystem
from CustomUseCase.serializers import CustomUseCaseSerializer
from CustomUseCase.toUML import UseCaseToUMLContext
from CustomUMLComponent.models import GrossularCustomUMLComponent
from CustomUMLComponent.serializers import GrossularCustomUMLComponentSerializer
from CustomUMLComponent.toUML import ComponentToUMLContext

from django.template.loader import render_to_string


class ProjectViewset(ViewSet):

    @action(detail=True, methods=['get'])
    def UseCase(self, request, pk):
        return Response(
            data=CustomUseCaseSerializer(GrossularCustomUseCase.grossular.inProject(pk), many=True).data)

    @action(detail=True, methods=['get'])
    def UseCaseUML(self, request, pk):
        #TODO: plot  by subsytem may (almost must) have some problem on parameter passing, please check it~
        subsystemList = request.query_params.dict().get('subsystem', None)
        UMLRendered = render_to_string('UseCasePlantUML.jinja2', UseCaseToUMLContext(pk, subsystemList))
        return Response(data={"UML": UMLRendered})

    @action(detail=True, methods=['get'])
    def Component(self, request, pk):
        return Response(
            data=GrossularCustomUMLComponentSerializer(GrossularCustomUMLComponent.grossular.inProject(pk),
                                                       many=True).data)

    @action(detail=True, methods=['get'])
    def ComponentUML(self, request, pk):
        packageList = request.query_params.getlist('package', None)
        packageList = packageList if len(packageList)>0 else None
        UMLRendered = render_to_string('ComponentPlantUML.jinja2', ComponentToUMLContext(pk, packageList))
        return Response(data={"UML": UMLRendered})

