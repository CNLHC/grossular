from grossularsphinx.abstract import PlantUMLDirective
from sphinx.util.docutils import SphinxDirective
import requests
import json
import grossularsphinx.api as API
import grossularsphinx.meta as groMeta
from docutils import nodes
import re

COMPONENT_REF_ID = "grossular-component-%d"


class ComponentContentNode(nodes.General, nodes.Element):
    pass


class ComponentInlineRefNode(nodes.General, nodes.Element):
    pass


class InterfaceContentNode(nodes.General, nodes.Element):
    pass


class InterfaceInlineRefNode(nodes.General, nodes.Element):
    pass


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

    def toNodes(self, jsobj):
        pass


class InterfaceContent(SphinxDirective):
    has_content = False

    def run(self):
        node = InterfaceContentNode('')


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
        defineList += self.toDefItem('提供接口', ','.join([i['name'] for i in jsobj['interfaces']]))
        return [targetnode, defineList]

    def toDefItem(self, key, value):
        item = nodes.definition_list_item()
        term = nodes.term(key, key)
        define = nodes.definition()
        define += nodes.paragraph(value, value)
        item += term
        item += define
        return item


def processComponentContent(app, doctree, fromdocname):
    env = app.builder.env
    for node in doctree.traverse(ComponentContentNode):
        groServer = app.config.grossular_server
        groProject = app.config.grossular_project
        print(node.grossularpackage)
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


def ComponentRefRole(role, rawtext, text, lineno, inliner,
                     options={}, content=[]):
    node = ComponentInlineRefNode('')
    namePattern = re.compile(":component:`(.*)`")
    codeName = re.match(namePattern, rawtext).group(1)
    node.meta = {
        'refCodeName': codeName
    }
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


def setup(app):
    app.add_node(ComponentContentNode)
    app.add_node(ComponentInlineRefNode)

    app.add_directive('componentuml', ComponentUML)
    app.add_directive('componentcontent', ComponentContent)
    app.add_directive('componentdetail', ComponentDetail)

    app.add_role('component', ComponentRefRole)
    app.connect('doctree-resolved', processComponentContent)
    app.connect('doctree-resolved', processComponentRefInline)

    return {
        'version': groMeta.version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
