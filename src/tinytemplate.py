"""Covert Template to Python Code
"""
import re

TOKENPATTERN = r"(?s)({{.*?}}|{%.*?%}|{#.*?#})"
LOGIC = "{%"
EXPRESSION = "{{"
COMMENT = "{#"

# TODO: this one should be configurable
INDENT_STEP = 4

class CodeBuilder:
    """Generate Python code
    """
    def __init__(self, indent=0):
        self.code = []
        self._indent_level = indent

    def indent(self):
        """ Increase the indent level """
        self._indent_level += INDENT_STEP

    def dedent(self):
        """ Decrease the indent level """
        self._indent_level -= INDENT_STEP

    def __str__(self):
        return "".join(str(s) for s in self.code)

    def add_line(self, line):
        """ add one line of code with indentation"""
        self.code.extend([" " * self._indent_level, line, "\n"])

    def add_section(self):
        section = CodeBuilder(self._indent_level)
        self.code.append(section)
        return section

    def get_globals(self):
        code_globals = dict()
        exec(str(self), code_globals)
        return code_globals

def do_dot(var, prop):
    try:
        return var.get(prop)
    except KeyError:
        return var[prop]

def dummy_function(*args):
    return 0

class TinyTemplate:
    def __init__(self, tepmplate, *contexts):
        
        self.template = tepmplate
        self.all_variables = set()
        self.loop_vars = set()
        self.render_code = dummy_function

        self.context = dict()
        for context in contexts:
            self.context.update(context)

    def _tokenize_templ(self):
        content = ''
        with open(self.template, 'r') as fp:
            content = fp.read()
        return re.split(TOKENPATTERN, content)
    
    def _expr_code(self, expr):
        self._variables(expr)
        code = f"c_{expr}"
        return code

    def _variables(self, var_name):
        # TODO: if var_name is a valid variable name?
        self.all_variables.add(var_name)
        

    def compiler(self):
        _code = CodeBuilder()

        _code.add_line("def render_code(context):")
        _code.indent()
        vars_code = _code.add_section()
        _code.add_line("result = list()")
        _code.add_line("extend_result = result.extend")
        _code.add_line("append_result = result.append")
        _code.add_line("to_str = str")

        buffer = list()
        def flush_output():
            if len(buffer) == 1:
                _code.add_line(f"append_result['{buffer[0]}']")
            elif len(buffer) > 1:
                _code.add_line(f'extend_result([{", ".join(buffer)}])')
            del buffer[:]

        templ_tokens = self._tokenize_templ()
        for token in templ_tokens:
            if token.startswith(COMMENT):
                continue
            if token.startswith(EXPRESSION):
                expr = self._expr_code(token[2:-2].strip())
                buffer.append(f"to_str({expr})")
                continue
            else:
                if token:
                    buffer.append(repr(token))
        flush_output()

        vars_code.add_line('print("Im ok")')

        _code.add_line("result_str = ''.join(result)")
        _code.add_line("return result_str")
        
        return _code.code

    def render(self, context=None):
        render_context = self.context
        if context:
            self.context.update(context)
        return self.render_code(render_context)
