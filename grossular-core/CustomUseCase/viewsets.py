from CustomUseCase.models import GrossularCustomUseCase
from rest_framework.viewsets import ModelViewSet
from CustomUseCase.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from Project.models import GrossularProject
from django.template.loader import render_to_string



class UseCaseViewset(ModelViewSet):
    serializer_class =   CustomUseCaseDetailSerializer
    queryset = GrossularCustomUseCase.objects.all()

    # def list(self, request, *args, **kwargs):
    #     projectName = request.query_params.dict().get('project', '')
    #     return Response(
    #         data=self.serializer_class(GrossularCustomUseCase.grossular.inProject(projectName), many=True).data)

    @action(methods=['GET'],detail=False)
    def plantuml(self,request):
        UMLRendered = render_to_string('UseCasePlantUML.jinja2', {
            'actors':['a','b','c'],
            'cases':['c','d','e'],
            'relationSet':['d','e']
        })
        return Response(data={"PlantUML":UMLRendered})














