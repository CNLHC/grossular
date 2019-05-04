from rest_framework.routers import SimpleRouter
from CustomUseCase.viewsets import UseCaseViewset
from CustomUMLComponent.viewsets import ComponentViewSet
from Project.viewsets import ProjectViewset

router =  SimpleRouter()

router.register('UseCase',UseCaseViewset)
router.register('Component',ComponentViewSet)
router.register('project',ProjectViewset,'project')

urlpatterns=router.urls
