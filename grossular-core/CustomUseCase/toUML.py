from CustomUseCase.models import GrossularCustomUseCase,GrossularCustomUseCaseSubsystem


def _handleSubsystem(caseQuerySets):
    actors=[]
    relationshipSet=[]
    useCase = []

    for case  in caseQuerySets: #type: GrossularCustomUseCase
        # handle association relationship
        for actor in case.association.all():
            actors.append(":{0}:".format(actor.name))
            relationshipSet.append("{actorName} --> ({caseName})".format(actorName=actor.name,caseName=case.name))

        # handle generalization relationship
        if case.generalization is not None:
            relationshipSet.append("({absName}) <|-- ({baseName})".format(absName=case.generalization.name,baseName=case.name))

        #handle include relationship
        for included in case.include.all():
            relationshipSet.append("({baseName}) ..> ({includedName}) : <<include>>".format(baseName=case.name,includedName=included.name))

        #handle extend relationship

        for extended in case.extend.all():
            relationshipSet.append("({extension}) ..> ({extended}) : <<extend>>".format(extension=case.name,extended=extended.name))


    return {
        'actors':actors,
        'relationSet':relationshipSet,
        'cases':useCase
    }



def UseCaseToUMLContext(projectCodeName,subsystemList=None):
    packages =[]
    actors=[]
    subsystemSets = GrossularCustomUseCaseSubsystem.grossular.inProject(projectCodeName)

    # generate by subsystem

    for subsystem in subsystemSets: #type:GrossularCustomUseCaseSubsystem
        if subsystemList is None or subsystem.codeName in  subsystemList:
            ctx=_handleSubsystem(subsystem.useCases.all())
            ctx['subsystemName'] = subsystem.name
            actors.extend(ctx['actors'])
            packages.append(ctx)

    # generate free casses
    freeCaseSets = GrossularCustomUseCase.grossular.inProject(projectCodeName).filter(subsystem=None)
    ctx = _handleSubsystem(freeCaseSets)
    ctx['subsystemName'] = None
    actors.extend(ctx['actors'])
    packages.append(ctx)

    actors=list(set(actors))

    return {
        "packages":packages,
        "actors":actors
    }


