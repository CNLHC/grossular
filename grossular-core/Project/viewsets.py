from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from CustomUseCase.models import GrossularCustomUseCase,GrossularCustomUseCaseSubsystem
from CustomUseCase.serializers import CustomUseCaseSerializer
from CustomUseCase.toUML import UseCaseToUMLContext

from django.template.loader import render_to_string

class ProjectViewset(ViewSet):

    @action(detail=True, methods=['get'])
    def UseCase(self, request,pk):
        return Response(
            data=CustomUseCaseSerializer(GrossularCustomUseCase.grossular.inProject(pk), many=True).data)

    @action(detail=True, methods=['get'])
    def UseCaseUML(self, request,pk):
        subsystemList = request.query_params.dict().get('subsystem',None)
        UMLRendered = render_to_string('UseCasePlantUML.jinja2', UseCaseToUMLContext(pk,subsystemList))
        return Response(data={"UML": UMLRendered})

