"""Covert Template to Python Code
"""
import re
import pathlib

TOKENPATTERN = r"(?s)({{.*?}}|{%.*?%}|{#.*?#})"
LOGIC = "{%"
EXPRESSION = "{{"
COMMENT = "{#"

# TODO: this one should be configurable
INDENT_STEP = 4

# templates/ folder should be same as this file.
TEMPLATE_DIR = pathlib.Path(__file__).resolve().parent

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
        source_code = str(self)
        print(source_code)
        exec(source_code, code_globals)
        return code_globals


def parser(var, *properties):
    """Parse x.y, or x.y.z while x is a dict

    The x.y.z is representing the structure of following
    context = {
        'x': {
            'y': {
                'z': 'hello'
            }
        }
    }
    return context['x']['y']['z']

    The x.y is representing the structure of following
    context = {
        'x': {
            'y': 'hello'
        }
    }
    return context['x']['y']
    
    :param var: the key of a context
    :type var: str
    :return: the value propery of var
    :rtype: Any
    """
    for prop in properties:
        try:
            var = getattr(var, prop)
        except AttributeError:
            var = var[prop]
    return var


def dummy_function(*args):
    return 0


class TinyTemplate:
    def __init__(self, template, *contexts):
        self.template = f'{str(TEMPLATE_DIR)}/templates/{template}'
        if pathlib.PurePath(template).is_absolute():
            self.template = template
        
        self._all_variables = set()
        self._loop_variables = set()
        self.dot_vars = set()
        self.render_code = dummy_function

        self.context = dict()
        for context in contexts:
            self.context.update(context)

    def compiler(self):
        _code = CodeBuilder()

        _code.add_line("def render_code(context, parser):")
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
        ops_stack = list()
        for token in templ_tokens:
            if token.startswith(COMMENT):
                continue
            elif token.startswith(EXPRESSION):
                expr = self._expr_code(token[2:-2].strip())
                buffer.append(f"to_str({expr})")
                continue
            elif token.startswith(LOGIC):
                flush_output()
                # FIXME: we only support one condition evaluation
                op, *expressions = token[2:-2].split()
                if op == 'if':
                    if len(expressions) == 0:
                        raise SyntaxError(f"Unknown syntax: if expression: `if {' '.join(expressions)}`")
                    print(f"expressions={expressions}")
                    expr = self._expr_code(' '.join(expressions))
                    ops_stack.append('if')
                    _code.add_line(f"if {expr}:")
                    _code.indent()
                elif op == 'for':
                    if len(expressions) < 3 or expressions[1] != 'in':
                        raise SyntaxError(f"Unknown syntax: for expression: `if {' '.join(expressions)}`")
                    print(f"expressions={expressions}")

                    loop_var, _, iter_var = expressions
                    self._add_loop_variables(loop_var)
                    # expr = self._expr_code(' '.join(expressions))
                    ops_stack.append('for')
                    _code.add_line(f"for c_{loop_var} in {self._expr_code(iter_var)}:")
                    _code.indent()
                elif op.startswith('end'):
                    end_op = op[3:]
                    print(f'current op stack:{ops_stack}')
                    print(f"ending op: {end_op}")
                    _code.dedent()
            else:
                if token:
                    buffer.append(repr(token))
        flush_output()
        for var_name in self._all_variables - self._loop_variables:
            vars_code.add_line(f'c_{var_name} = context["{var_name}"]')

        _code.add_line("result_str = ''.join(result)")
        _code.add_line("return result_str")

        return _code

    def _tokenize_templ(self):
        content = ''
        with open(self.template) as fp:
            content = fp.read()
        return re.split(TOKENPATTERN, content)

    def _expr_code(self, expr):
        code = ''
        if '.' in expr:
            var, *property_ = expr.split('.')
            code = self._expr_code(var)
            args = ", ".join(repr(d) for d in property_)
            code = f"parser(c_{var}, {args})"
            print(code)
            print(self.dot_vars)
        else:
            self._add_all_variables(expr)
            code = f"c_{expr}"
        return code

    def _add_all_variables(self, var_name):
        # TODO: if var_name is a valid variable name?
        self._all_variables.add(var_name)

    def _add_loop_variables(self, var_name):
        self._loop_variables.add(var_name)

    def render(self, context=None):
        render_context = self.context
        if context:
            self.context.update(context)
        codeobj = self.compiler()
        source_code = ''.join(str(s) for s in codeobj.code)
        print(source_code)
        source_code_globals = dict()
        exec(source_code, source_code_globals)
        self.render_code = source_code_globals['render_code']
        return self.render_code(render_context, parser)
