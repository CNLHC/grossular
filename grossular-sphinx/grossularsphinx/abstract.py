import os
from docutils import nodes
from sphinx.util.docutils import SphinxDirective
import sphinxcontrib.plantuml  as splantuml
from sphinx.util.nodes import set_source_info


class PlantUMLDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 10000
    option_spec = splantuml.UmlDirective.option_spec

    def genImageNode(self,rawPlantuml:str):
        env = self.env
        relfn = env.doc2path(env.docname, base=None)
        node = splantuml.plantuml(self.block_text, **self.options)
        node['uml'] = rawPlantuml
        node['incdir'] = os.path.dirname(relfn)
        node['filename'] = os.path.split(relfn)[1]
        if 'caption' in self.options or 'align' in self.options:
            node = nodes.figure('', node)
            if 'align' in self.options:
                node['align'] = self.options['align']
        if 'caption' in self.options:
            inodes, messages = self.state.inline_text(self.options['caption'],
                                                      self.lineno)
            caption_node = nodes.caption(self.options['caption'], '', *inodes)
            caption_node.extend(messages)
            set_source_info(self, caption_node)
            node += caption_node
        if 'html_format' in self.options:
            node['html_format'] = self.options['html_format']
        if 'latex_format' in self.options:
            node['latex_format'] = self.options['latex_format']
        return node

    