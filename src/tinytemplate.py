"""Covert Template to Python Code
"""
import re

from compiler import CodeBuilder

TOKENPATTERN = r"(?s)({{.*?}}|{%.*?%}|{#.*?#})"
LOGIC = "{%"
EXPRESSION = "{{"
COMMENT = "{#"
class TinyTemplate:
    def __init__(self):
        self.code = CodeBuilder()

    def _tokenize_templ(self, templ_file):
        content = ''
        with open(templ_file, 'r') as fp:
            content = fp.read()
        return re.split(TOKENPATTERN, content)

    def render(self, templ_file, *context):
        templ = self._tokenize_templ(templ_file)
