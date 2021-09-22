"""Covert Template to Python Code
"""
import re
import pathlib
from __future__ import annotations # pospone evaluation for type hints
from typing import Any, Dict, List, Mapping, MutableSet, NoReturn, Optional, Sequence

TOKENPATTERN = r"(?s)({{.*?}}|{%.*?%}|{#.*?#})"

# TODO: this one should be configurable
INDENT_STEP = 4

# templates/ folder should be same as this file.
TEMPLATE_DIR = pathlib.Path(__file__).resolve().parent

class CodeBlock:
    """Generate Python code
    """
    def __init__(self, indent: int = 0) -> None:
        self.code: List[str] = []
        self._indent_level = indent

    def indent(self) -> None:
        """ Increase the indent level """
        self._indent_level += INDENT_STEP

    def dedent(self) -> None:
        """ Decrease the indent level """
        self._indent_level -= INDENT_STEP

    def __str__(self):
        return "".join(str(s) for s in self.code)

    def add_line(self, line: str) -> None:
        """ add one line of code with indentation"""
        self.code.extend([" " * self._indent_level, line, "\n"])

    def add_section(self) -> CodeBlock:
        section = CodeBlock(self._indent_level)
        self.code.append(str(section))
        return section

    def get_globals(self) -> Dict[str, str]:
        code_globals: Dict[str, str] = dict()
        source_code = str(self)
        print(source_code)
        exec(source_code, code_globals)
        return code_globals


def parse_template_file(template: str) -> List[str]:
    content = ''
    with open(template) as fp:
        content = fp.read()
    return re.split(TOKENPATTERN, content)


def dot(var: Mapping[str, Any], *properties: str) -> Any:
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
    :return: the value property of var
    :rtype: Any
    """
    for prop in properties:
        try:
            var = getattr(var, prop)
        except AttributeError:
            var = var[prop]
    return var


class TinyTemplate:
    def __init__(self, template: str, *contexts):
        self._template = f'{str(TEMPLATE_DIR)}/templates/{template}'
        if pathlib.PurePath(template).is_absolute():
            self._template = template

        self._buffer: List[Any] = list()
        self._ops_stack: List[Any] = list()

        self._context: Dict[str, Any] = dict()
        self._all_variables: MutableSet[str] = set()
        self._loop_variables: MutableSet[str] = set()
        self._code = CodeBlock()
        self._templ_tokens = parse_template_file(self._template)

    def render(self, context: Optional[Dict[str, Any]] = None):
        render_context = self._context
        if context:
            render_context.update(context)
        codeobj = self._compile_to_pycode()
        source_code = ''.join(str(s) for s in codeobj.code)
        print(source_code)
        # Use for storing globals in source_code_globals
        source_code_globals: Dict[str, Any] = dict()
        exec(source_code, source_code_globals)
        self.code_runner = source_code_globals['render_code']
        return self.code_runner(render_context, dot)

    def _compile_to_pycode(self) -> CodeBlock:
        self._code.add_line("def render_code(context, dot):")
        self._code.indent()
        self._vars_code = self._code.add_section()
        self._code.add_line("result = list()")
        self._code.add_line("extend_result = result.extend")
        self._code.add_line("append_result = result.append")
        self._code.add_line("to_str = str")
        self._template_token_analyze()
        self._handling_global_variables()
        self._code.add_line("result_str = ''.join(result)")
        self._code.add_line("return result_str")

        return self._code

    def _handling_global_variables(self) -> None:
        for var_name in self._all_variables - self._loop_variables:
            self._vars_code.add_line(f'c_{var_name} = context["{var_name}"]')

    def flush_buffer(self) -> None:
        if len(self._buffer) == 1:
            self._code.add_line(f"append_result({self._buffer[0]})")
        elif len(self._buffer) > 1:
            self._code.add_line(f'extend_result([{", ".join(self._buffer)}])')
        del self._buffer[:]

    def _template_token_analyze(self) -> None:
        # FIXME: handle the damn multiple CRs, current output sucks.
        for token in self._templ_tokens:
            # Ignore comment lines
            if token.startswith(r"{#"):
                continue
            elif token.startswith(r"{{"):
                self._handling_variable_evaluation(token)
            elif token.startswith(r"{%"):
                self._handling_logic_control_statements(token)
            else:
                if token:
                    self._buffer.append(repr(token))
        self.flush_buffer()

    def _handling_variable_evaluation(self, token: str) -> None:
        stmt_code = self._generate_statement_code(token[2:-2].strip())
        self._buffer.append(f"to_str({stmt_code})")

    def _handling_logic_control_statements(self, token: str) -> None:
        self.flush_buffer()
        # FIXME: we only support one condition evaluation
        # Extract statement first, [2:-2] to strip {%...%} marker
        op, *expressions = token[2:-2].split()

        if op == 'if':
            self._if_statement(expressions)
        elif op == 'for':
            self._for_statement(expressions)
        elif op.startswith('end'):
            self._end_statement()

    def _if_statement(self, expressions: List[str]) -> None:
        if len(expressions) == 0:
            raise SyntaxError(f"Unknown syntax: if expression: `if {' '.join(expressions)}`")
        expr = self._generate_statement_code(' '.join(expressions))
        self._ops_stack.append('if')
        self._code.add_line(f"if {expr}:")
        self._code.indent()

    def _for_statement(self, expressions: List[str]) -> None:
        # for loop should be `for x in y`
        if len(expressions) < 3 or expressions[1] != 'in':
            raise SyntaxError(f"Unknown syntax: for expression: `if {' '.join(expressions)}`")

        loop_var, _, iter_var = expressions
        self._add_loop_variables(loop_var)

        self._ops_stack.append('for')
        self._code.add_line(f"for c_{loop_var} in {self._generate_statement_code(iter_var)}:")
        self._code.indent()

    def _end_statement(self) -> None:
        # TODO: end_op = op[3:] need error handling
        self._code.dedent()

    def _generate_dot_code(self, expr: str) -> str:
        """Convert "var.property" to "dot(var, "property")"

        Multiple dots supported, too.

        var.property1.property2.property3

        will be converted to:

        dot(var, "property1", "property2", "property3")
        
        :param expr: dotted variables
        :type expr: str
        :return: generate the dot() code
        :rtype: str
        """
        var, *property_ = expr.split('.')
        self._add_all_variables(var)
        args = ", ".join(repr(d) for d in property_)
        return f"dot(c_{var}, {args})"

    def _generate_pipe_code(self, expr: str) -> str:
        """Convert "var|func1|func2" to "c_func2(c_func1(c_var))"

        :param expr: pipe variables
        :type expr: str
        :return: generate corresponding function call code
        :rtype: str
        """
        var, *funcs = expr.split('|')
        code = self._generate_statement_code(var)
        for _func in funcs:
            self._add_all_variables(_func)
            code = f"c_{_func}({code})"
        return code

    def _generate_var_code(self, expr: str) -> str:
        """Convert "var" to "c_var"

        :param expr: variable name
        :type expr: str
        :return: generate c_ prefix code
        :rtype: str
        """
        self._add_all_variables(expr)
        return f"c_{expr}"

    def _generate_statement_code(self, expr: str) -> str:
        code = ''
        # `|`` pipes must be parsed before `.` dots parsed due to evaluation order
        if '|' in expr:
            code = self._generate_pipe_code(expr)
        elif '.' in expr:
            code = self._generate_dot_code(expr)
        else:
            code = self._generate_var_code(expr)
        return code

    def _add_all_variables(self, var_name: str) -> None:
        # TODO: if var_name is a valid variable name?
        self._all_variables.add(var_name)

    def _add_loop_variables(self, var_name: str) -> None:
        self._loop_variables.add(var_name)

