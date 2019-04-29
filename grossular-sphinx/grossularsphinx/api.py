import urllib

UseCaseDetail =  lambda server,project:'{0}/api/UseCase/{1}/'.format(server,project)
UseCaseListAll =  lambda server,project:'{0}/api/project/{1}/UseCase/'.format(server,project)

def UseCaseUml(server:str,project:str,subsystemList=[]):
    query = urllib.parse.urlencode({"subsystem":subsystemList}) if len(subsystemList)>0 else ''
    return '{0}/api/project/{1}/UseCaseUML/?{2}'.format(server,project,query)

    




