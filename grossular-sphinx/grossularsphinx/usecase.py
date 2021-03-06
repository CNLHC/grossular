from docutils import nodes
from grossularsphinx.abstract import PlantUMLDirective
from sphinx.util.docutils import SphinxDirective
import grossularsphinx.api as API
import grossularsphinx.meta as groMeta
import requests
import json

REF_ID = "grossular-usecase-%d"


class UseCaseDetailListDirective(SphinxDirective):
    has_content = False

    def run(self):
        groServer = self.config.grossular_server
        groProject = self.config.grossular_project
        res = requests.get(API.UseCaseListAll(groServer, groProject))
        res.encoding = "utf8"
        jsobj = json.loads(res.text)
        nodeList = []
        self.info("grossular: read {caseCount} cases".format(
            caseCount=len(jsobj)))
        for caseObj in jsobj:
            caseDetailObj = json.loads(requests.get(
                API.UseCaseDetail(groServer, caseObj['id'])).text)
            targetid = REF_ID % caseObj['id']
            nodeList.append(nodes.target('', '', ids=[targetid]))
            admonBar = nodes.admonition()
            admonBar += nodes.title('admonTitle', "用例名称")
            admonBar += nodes.paragraph('caseName', caseObj['name'])
            nodeList.append(admonBar)
            nodeList.append(nodes.paragraph(
                "caseComment", caseObj['comments']))
            nodeList.extend(self.genCaseCrossRefNodes(caseDetailObj=caseDetailObj,
                                                      crossFieldName='concrete',
                                                      crossTitle='具体用例参见:'))
            nodeList.extend(self.genCaseCrossRefNodes(caseDetailObj=caseDetailObj,
                                                      crossFieldName='extension',
                                                      crossTitle='该用例功能被以下用例扩展:'))
            nodeList.extend(self.genCaseCrossRefNodes(caseDetailObj=caseDetailObj,
                                                      crossFieldName='include',
                                                      crossTitle='该用例包括以下子用例:'))
        return nodeList

    def genCaseCrossRefNodes(self, caseDetailObj, crossFieldName, crossTitle):
        nodeList = []
        if len(caseDetailObj[crossFieldName]) > 0:
            nodeList.append(nodes.paragraph(crossTitle, crossTitle))
            relationCaseList = nodes.bullet_list()
            for relationCase in caseDetailObj[crossFieldName]:
                ref = nodes.reference('', '')
                ref.append(nodes.Text(
                    relationCase['name'], relationCase['name']))
                ref['refuri'] = '#' + REF_ID % relationCase['id']
                para = nodes.paragraph('', '')
                para += ref
                listItem = nodes.list_item('')
                listItem.append(para)
                relationCaseList.append(listItem)
            nodeList.append(relationCaseList)
        return nodeList


class UseCaseContent(SphinxDirective):
    def run(self):
        groServer = self.config.grossular_server
        groProject = self.config.grossular_project
        res = requests.get(API.UseCaseListAll(groServer, groProject))
        jsobj = json.loads(res.text)
        nodeList = []
        ContentList = nodes.bullet_list()
        for caseObj in jsobj:
            ref = nodes.reference('', '')
            ref.append(nodes.Text(
                caseObj['name'], caseObj['name']))
            ref['refuri'] = '#' + REF_ID % caseObj['id']
            para = nodes.paragraph('', '')
            para += ref
            listItem = nodes.list_item('')
            listItem.append(para)
            ContentList.append(listItem)
        nodeList.append(ContentList)
        return nodeList


class UseCaseUML(PlantUMLDirective):
    has_content = False

    def run(self):
        groServer = self.config.grossular_server
        groProject = self.config.grossular_project
        res = requests.get(API.UseCaseUml(groServer, groProject, subsystemList=self.arguments))
        res.encoding = "utf8"
        jsobj = json.loads(res.text)
        return [self.genImageNode(jsobj['UML'])]


def setup(app):
    app.add_directive('usecasedetaillist', UseCaseDetailListDirective)
    app.add_directive('usecaseuml', UseCaseUML)
    app.add_directive('usecasecontent', UseCaseContent)
    app.add_config_value('grossular_server', 'http://127.0.0.1:8000', 'html')
    app.add_config_value('grossular_project', '', 'html')
    return {
        'version': groMeta.version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
