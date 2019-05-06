from grossularsphinx.abstract import PlantUMLDirective
from sphinx.util.docutils import SphinxDirective
import requests
import json
import grossularsphinx.api as API
import grossularsphinx.meta as groMeta
from docutils import nodes
import re

COMPONENT_REF_ID = "grossular-component-%d"
INTERFACE_REF_ID = "grossular-interface-%d"


class ComponentContentNode(nodes.General, nodes.Element):
    pass


class ComponentInlineRefNode(nodes.General, nodes.Element):
    # todo: using refCodeName is a bad idea here, should migrate to something like refId
    def __init__(self, componentCodeName):
        super().__init__('')
        self.meta = {
            'refCodeName': componentCodeName
        }


class InterfaceContentNode(nodes.General, nodes.Element):
    pass


class InterfaceInlineRefNode(nodes.General, nodes.Element):
    def __init__(self, refId,name):
        super().__init__('')
        self.meta = {
            'refId': refId,
            'name':name

        }


class ComponentUML(PlantUMLDirective):
    has_content = False

    def run(self):
        groServer = self.config.grossular_server
        groProject = self.config.grossular_project
        res = requests.get(API.ComponentUML(groServer, groProject, packageList=self.arguments),
                           params={"package": self.arguments})
        res.encoding = "utf8"
        jsobj = json.loads(res.text)
        return [self.genImageNode(jsobj['UML'])]


class ComponentContent(SphinxDirective):
    has_content = False
    optional_arguments = 1

    def run(self):
        node = ComponentContentNode('')
        node.grossularpackage = None if len(self.arguments) == 0 else self.arguments[0]
        return [node]


class InterfaceContent(SphinxDirective):
    has_content = False
    optional_arguments = 1

    def run(self):
        node = InterfaceContentNode('')
        node.grossularpackage = None if len(self.arguments) == 0 else self.arguments[0]
        return [node]


class ComponentDetail(SphinxDirective):
    has_content = False
    required_arguments = 1

    def run(self):
        groServer = self.config.grossular_server
        groProject = self.config.grossular_project
        res = requests.get(API.ComponentList(groServer), params={
            "grossularProject__codeName": groProject,
            "codeName": self.arguments[0]
        })
        if not hasattr(self.env, 'grossularComponentDetailed'):
            self.env.grossularComponentDetailed = []
        try:
            jsobj = json.loads(res.text)[0]
            detailNodes = self.toNodes(jsobj)
            self.env.grossularComponentDetailed.append({
                'docname': self.env.docname,
                'refId': COMPONENT_REF_ID % jsobj['id'],
                'name': jsobj['name'],
                'codeName': jsobj['codeName']
            })
            return detailNodes

        except IndexError:
            return [nodes.Text('something wrong', 'something wrong')]

    def toNodes(self, jsobj):
        targetid = COMPONENT_REF_ID % jsobj['id']
        targetnode = nodes.target('', '', ids=[targetid])
        defineList = nodes.definition_list()
        defineList += self.toDefItem('组件名称', jsobj['name'])
        defineList += self.toDefItem('组件代号', jsobj['codeName'])

        para = nodes.paragraph()
        IList = self.toInterfaceList(jsobj['interfaces'])
        para+=IList
        defineList += self.toDefItem('提供接口', Paragraph=para)

        return [targetnode, defineList]

    def toDefItem(self, key, value='', Paragraph=None):
        item = nodes.definition_list_item()
        term = nodes.term(key, key)
        define = nodes.definition()
        if Paragraph is None:
            define += nodes.paragraph(value, value)
        else:
            define += Paragraph
        item += term
        item += define
        return item

    def toInterfaceList(self, interfaceList):
        InterfaceList = nodes.bullet_list()
        for Interface in interfaceList:
            listItem = nodes.list_item()
            para = nodes.paragraph()
            para += InterfaceInlineRefNode(refId=INTERFACE_REF_ID % Interface['id'],name=Interface['name'])
            listItem += para
            InterfaceList.append(listItem)
        return InterfaceList


class InterfaceDetail(SphinxDirective):
    has_content = False
    required_arguments = 2

    def run(self):
        groServer = self.config.grossular_server
        groProject = self.config.grossular_project
        res = requests.get(API.InterfaceList(groServer), params={
            "grossularProject__codeName": groProject,
            'Component__codeName': self.arguments[0],
            "name": self.arguments[1]
        })
        if not hasattr(self.env, 'grossularInterfaceDetailed'):
            self.env.grossularInterfaceDetailed = []

        jsobj = json.loads(res.text)[0]  # type:dict
        jsobj['Component'] = json.loads(requests.get(API.ComponentDetail(groServer, jsobj['Component'])).text)
        jsobj['InvokingComponentList'] = json.loads(requests.get(API.ComponentList(groServer), params={
            "grossularProject__codeName": groProject,
            "using__interface__id": jsobj['id']
        }).text)
        detailNodes = self.toNodes(jsobj)
        self.env.grossularInterfaceDetailed.append({
            'docname': self.env.docname,
            'refId': INTERFACE_REF_ID % jsobj['id'],
            'name': jsobj['name'],
            'obj': jsobj
        })
        return detailNodes

    def toNodes(self, jsobj):
        targetid = INTERFACE_REF_ID% jsobj['id']
        targetnode = nodes.target('', '', ids=[targetid])
        defineList = nodes.definition_list()
        defineList += self.toDefItem('接口名称', value=jsobj['name'])
        defineList += self.toDefItem('接口ID', value=jsobj['id'])

        para = nodes.paragraph('', '')
        ref = ComponentInlineRefNode(componentCodeName=jsobj['Component']['codeName'])
        para += ref
        defineList += self.toDefItem('组件名称', Paragraph=para)

        para = nodes.paragraph('', '')
        invokingList = self.toInvolingList(jsobj['InvokingComponentList'])
        para += invokingList
        defineList += self.toDefItem('被以下组件调用', Paragraph=para)

        return [targetnode, defineList]

    def toDefItem(self, key, value='', Paragraph=None):
        item = nodes.definition_list_item()
        term = nodes.term(key, key)
        define = nodes.definition()
        if Paragraph is None:
            define += nodes.paragraph(value, value)
        else:
            define += Paragraph
        item += term
        item += define
        return item

    def toInvolingList(self, involingList):
        ComponentList = nodes.bullet_list()
        for component in involingList:
            listItem = nodes.list_item('')
            para = nodes.paragraph('', '')
            para += ComponentInlineRefNode(componentCodeName=component['codeName'])
            listItem += para
            ComponentList.append(listItem)
        return ComponentList


def processComponentContent(app, doctree, fromdocname):
    env = app.builder.env
    for node in doctree.traverse(ComponentContentNode):
        groServer = app.config.grossular_server
        groProject = app.config.grossular_project
        res = requests.get(API.ComponentList(groServer), params={
            "grossularProject__codeName": groProject,
            "package__name": node.grossularpackage
        })
        jsobj = json.loads(res.text)

        nodeList = []
        detailedComponent = {}
        for item in env.grossularComponentDetailed:
            detailedComponent[item['refId']] = item

        ContentList = nodes.bullet_list()
        for component in jsobj:
            name = '{name}({codeName})'.format(name=component['name'], codeName=component['codeName'])
            refId = COMPONENT_REF_ID % component['id']
            detailedObj = detailedComponent.get(refId, None)
            if detailedObj is None:
                para = nodes.paragraph(name, name)
            else:
                newnode = nodes.reference('', '')
                newnode['refdocname'] = detailedObj['docname']
                newnode['refuri'] = app.builder.get_relative_uri(
                    fromdocname, detailedObj['docname'])
                newnode['refuri'] += '#' + refId
                newnode.append(nodes.Text(name, name))
                para = nodes.paragraph('', '')
                para += newnode
            listItem = nodes.list_item('')
            listItem.append(para)
            ContentList.append(listItem)
        nodeList.append(ContentList)
        node.replace_self(nodeList)
    return


def processInterfaceContent(app, doctree, fromdocname):
    env = app.builder.env
    for node in doctree.traverse(InterfaceContentNode):
        groServer = app.config.grossular_server
        groProject = app.config.grossular_project
        res = requests.get(API.InterfaceList(groServer), params={
            "grossularProject__codeName": groProject,
            "Component__package__name": node.grossularpackage
        })
        jsonobj = json.loads(res.text)

        detailedInterface = {}
        if not hasattr(env, 'grossularInterfaceDetailed'):
            env.grossularInterfaceDetailed = []

        for item in env.grossularInterfaceDetailed:
            detailedInterface[item['refId']] = item

        ContentList = nodes.bullet_list()
        for interface in jsonobj:
            name = '({d})-{name}'.format(name=interface['name'], d=interface['id'])
            refId = INTERFACE_REF_ID % interface['id']
            detailedObj = detailedInterface.get(refId, None)
            if detailedObj is None:
                para = nodes.paragraph(name, name)
            else:
                newnode = nodes.reference('', '')
                newnode['refdocname'] = detailedObj['docname']
                newnode['refuri'] = app.builder.get_relative_uri(
                    fromdocname, detailedObj['docname'])
                newnode['refuri'] += '#' + refId
                newnode.append(nodes.Text(name, name))
                para = nodes.paragraph('', '')
                para += newnode
            listItem = nodes.list_item('')
            listItem.append(para)
            ContentList.append(listItem)
        node.replace_self([ContentList])
    return


def ComponentRefRole(role, rawtext, text, lineno, inliner,
                     options={}, content=[]):
    node = ComponentInlineRefNode('')
    namePattern = re.compile(":component:`(.*)`")
    codeName = re.match(namePattern, rawtext).group(1)
    node.meta = {
        'refCodeName': codeName
    }
    return [node], []


def InterfaceRefRole(role, rawtext, text, lineno, inliner,
                     options={}, content=[]):
    #TODO: using id here seems inconveninet for user, but useing name seems inconveninent for code.
    #TODO: need more design

    node = ComponentInlineRefNode('')
    namePattern = re.compile(":interface:`(.*)`")
    codeName = re.match(namePattern, rawtext).group(1)
    return [node], []


def processComponentRefInline(app, doctree, fromdocname):
    env = app.builder.env
    for node in doctree.traverse(ComponentInlineRefNode):
        if not hasattr(env, 'grossularComponentDetailed'):
            env.grossularComponentDetailed = []

        detailedComponent = {}
        for item in env.grossularComponentDetailed:
            detailedComponent[item['codeName']] = item

        detailedList = env.grossularComponentDetailed
        detailed = [i for i in detailedList if i['codeName'] == node.meta['refCodeName']]

        if len(detailed) > 0:
            detailedObj = detailed[0]
            newnode = nodes.reference('', '')
            newnode['refdocname'] = detailedObj['docname']
            newnode['refuri'] = app.builder.get_relative_uri(
                fromdocname, detailedObj['docname'])
            newnode['refuri'] += '#' + detailedObj['refId']
            newnode.append(nodes.Text('组件:' + detailedObj['name'], '组件:' + detailedObj['name']))
        else:
            newnode = nodes.Text('组件:' + node.meta['refCodeName'], '组件:' + node.meta['refCodeName'])

        node.replace_self(newnode)


def processInterfaceRefInline(app, doctree, fromdocname):
    env = app.builder.env
    detailedInterface = {}
    for item in env.grossularInterfaceDetailed:
        detailedInterface[item['refId']] = item

    for node in doctree.traverse(InterfaceInlineRefNode):
        if not hasattr(env, 'grossularInterfaceDetailed'):
            env.grossularInterfaceDetailed = []

        detailedList = env.grossularInterfaceDetailed
        detailed = [i for i in detailedList if  i['refId'] == node.meta['refId']]

        if len(detailed) > 0:
            detailedObj = detailed[0]
            newnode = nodes.reference('', '')
            newnode['refdocname'] = detailedObj['docname']
            newnode['refuri'] = app.builder.get_relative_uri(
                fromdocname, detailedObj['docname'])
            newnode['refuri'] += '#' + detailedObj['refId']
            newnode.append(nodes.Text('接口:' + detailedObj['name'], '接口:' + detailedObj['name']))
        else:
            newnode = nodes.Text('接口:' + node.meta['name'], '接口:' + node.meta['name'])

        node.replace_self(newnode)


def setup(app):
    app.add_node(ComponentContentNode)
    app.add_node(ComponentInlineRefNode)
    app.add_node(InterfaceContentNode)

    app.add_directive('componentuml', ComponentUML)
    app.add_directive('componentcontent', ComponentContent)
    app.add_directive('componentdetail', ComponentDetail)
    app.add_directive('interfacecontent', InterfaceContent)
    app.add_directive('interfacedetail', InterfaceDetail)

    app.add_role('component', ComponentRefRole)
    app.connect('doctree-resolved', processComponentContent)
    app.connect('doctree-resolved', processComponentRefInline)
    app.connect('doctree-resolved', processInterfaceContent)
    app.connect('doctree-resolved', processInterfaceRefInline)

    return {
        'version': groMeta.version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
