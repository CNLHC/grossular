from .models import GrossularCustomUMLComponent, GrossularCustomUMLComponentPackage, \
    GrossularCustomUMLComponentInterface


def _handlePackage(componentSet):
    componentList = []
    associationList = []
    innerInvokeList = []
    interfaceList = []
    outInvokeCtx = []
    for component in componentSet:  # type:GrossularCustomUMLComponent
        componentList.append("[{name}]".format(name=component.name))

        # using interface.__str__() to get
        for interface in component.interfaces.all():
            associationList.append(
                "{interface} - [{component}]".format(interface=interface.uniqueName(), component=component.name))

            interfaceList.append(
                '() "{interface}" as {uniquename}'.format(interface=interface.name, uniquename=interface.uniqueName()))

        for using in component.using.all():
            record = "[{component}] --> {interface}".format(component=component.name,
                                                            interface=using.interface.uniqueName())
            innerInvokeList.append(record)

            if using.interface.Component.package.id != component.package.id:
                outInvokeCtx.append((using.interface.Component.package, using.interface))

    return {
        'interfaces': interfaceList,
        'components': componentList,
        'associations': associationList,
        'invokeList': innerInvokeList,
        'meta': outInvokeCtx
    }


def ComponentToUMLContext(projectCodeName, packageList=None):
    ctxList = []
    componentSet = GrossularCustomUMLComponent.grossular.inProject(projectCodeName)
    packageQuery = GrossularCustomUMLComponentPackage.grossular.inProject(projectCodeName)

    if packageList is not None:
        all = GrossularCustomUMLComponentPackage.grossular.inProject(projectCodeName)
        packageQuery = GrossularCustomUMLComponentPackage.objects.none()
        for pack in packageList:
            packageQuery = packageQuery | all.filter(name=pack)

    for package in packageQuery:  # type:GrossularCustomUMLComponentPackage
        tSet = componentSet.filter(package__name=package.name)
        if tSet.count() > 0:
            ctx = _handlePackage(tSet)
            ctx['packageName'] = package.name
            ctx['shape'] = package.shape
            ctxList.append(ctx)

    outerList = []
    for pack in ctxList:
        for tPackage, tInterface in pack[
            'meta']:  # type:(GrossularCustomUMLComponentPackage,GrossularCustomUMLComponentInterface)
            if  packageList is not None and tPackage.name not in packageList:
                outerList.append(
                    '() "{interface}" as {uniquename}'.format(interface=tInterface.name,
                                                              uniquename=tInterface.uniqueName()))

    return {"packages": ctxList,
            "outerInterfaces": outerList
            }

    # generate by subsystem
