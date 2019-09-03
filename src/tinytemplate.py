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
    
    def render_expression(self, value):
        self.code.add_line(value)
        print(self.code.code)
        return str(self.code)

    def render(self, templ_file, context):
        templ_tokens = self._tokenize_templ(templ_file)
        
        buffer = list()
        for token in templ_tokens:
            if token.startswith(COMMENT):
                continue
            if token.startswith(EXPRESSION):
                buffer.extend(self.render_expression(context))
                continue
            buffer.append(token)
        return buffer
