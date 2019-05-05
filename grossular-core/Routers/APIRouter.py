from rest_framework.routers import SimpleRouter
from CustomUseCase.viewsets import UseCaseViewset
from CustomUMLComponent.viewsets import ComponentViewSet, InterfaceViewSet
from Project.viewsets import ProjectViewset

router = SimpleRouter()

router.register('UseCase', UseCaseViewset)
router.register('Component', ComponentViewSet)
router.register('Interface', InterfaceViewSet)
router.register('project', ProjectViewset, 'project')

urlpatterns = router.urls
