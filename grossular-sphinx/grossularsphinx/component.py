from grossularsphinx.abstract import PlantUMLDirective
import requests
import json
import grossularsphinx.api as API
import grossularsphinx.meta as groMeta


class ComponentUML(PlantUMLDirective):
    has_content = False

    def run(self):
        groServer = self.config.grossular_server
        groProject = self.config.grossular_project
        res = requests.get(API.ComponentUML(groServer, groProject, packageList=self.arguments),params={"package":self.arguments})
        res.encoding = "utf8"
        jsobj = json.loads(res.text)
        return [self.genImageNode(jsobj['UML'])]


def setup(app):
    app.add_directive('componentuml', ComponentUML)
    return {
        'version': groMeta.version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
