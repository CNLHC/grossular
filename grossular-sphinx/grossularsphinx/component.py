from grossularsphinx.abstract import PlantUMLDirective
from sphinx.util.docutils import SphinxDirective
import requests
import json
import grossularsphinx.api as API
import grossularsphinx.meta as groMeta
from docutils import nodes

COMPONENT_REF_ID = "grossular-component-%d"


class ComponentContentNode(nodes.General, nodes.Element):
    pass


def processComponentContent(app, doctree, fromdocname):
    env = app.builder.env
    for node in doctree.traverse(ComponentContentNode):
        if not app.config.todo_include_todos:
            node.replace_self([])
            continue

        groServer = app.config.grossular_server
        groProject = app.config.grossular_project
        res = requests.get(API.ComponentList(groServer, groProject), params={"package": node.grossularpackage})
        jsobj = json.loads(res.text)
        nodeList = []

        if not hasattr(env, 'grossularComponentDetailed'):
            env.grossularComponentDetailed = []

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


class ComponentDetail(SphinxDirective):
    has_content = False
    required_arguments = 1

    def run(self):
        groServer = self.config.grossular_server
        groProject = self.config.grossular_project
        if not hasattr(self.env, 'grossularComponentList'):
            res = requests.get(API.ComponentList(groServer, groProject))
            jsobj = json.loads(res.text)
            self.env.grossularComponentList = jsobj

        detailObj = [i for i in self.env.grossularComponentList if i['codeName'] == self.arguments[0]]

        if len(detailObj) == 0:
            self.error(" grossular : can not find component named '{name}'".format(name=self.arguments))
        elif len(detailObj) > 1:
            self.error(" grossular : find multiple instance of  '{name}'".format(name=self.arguments))

        detailObjId = detailObj[0]['id']
        res = requests.get(API.ComponentDetail(groServer, detailObjId))
        jsobj = json.loads(res.text)

        if not hasattr(self.env, 'grossularComponentDetailed'):
            self.env.grossularComponentDetailed = []
        detailNodes = self.toNodes(jsobj)

        self.env.grossularComponentDetailed.append({
            'docname': self.env.docname,
            'refId': COMPONENT_REF_ID % jsobj['id']
        })

        return detailNodes

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


def setup(app):
    app.add_directive('componentuml', ComponentUML)
    app.add_directive('componentcontent', ComponentContent)
    app.add_directive('componentdetail', ComponentDetail)

    app.add_node(ComponentContentNode)
    app.connect('doctree-resolved', processComponentContent)

    return {
        'version': groMeta.version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
