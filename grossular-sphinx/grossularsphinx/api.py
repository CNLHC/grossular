import urllib

UseCaseDetail = lambda server, project: '{0}/api/UseCase/{1}/'.format(server, project)
UseCaseListAll = lambda server, project: '{0}/api/project/{1}/UseCase/'.format(server, project)
ComponentList = lambda server: '{0}/api/Component/'.format(server)
InterfaceList= lambda server: '{0}/api/Interface/'.format(server)
ComponentDetail = lambda server,id: '{0}/api/Component/{1}/'.format(server,id)


def UseCaseUml(server: str, project: str, subsystemList=[]):
    query = urllib.parse.urlencode({"subsystem": subsystemList}) if len(subsystemList) > 0 else ''
    return '{0}/api/project/{1}/UseCaseUML/?{2}'.format(server, project, query)


def ComponentUML(server: str, project: str, packageList=[]):
    return '{0}/api/project/{1}/ComponentUML/'.format(server, project)
