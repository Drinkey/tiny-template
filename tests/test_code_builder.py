import tinytemplate
import pytest


@pytest.fixture(scope="function", autouse=True)
def setup_function():
    pass


codesource = """
import re
import os

var1 = 123
var_str = 'unittest'

def func_1():
    return 1

"""


def test_compiler_add_multiple_lines():
    code_line = [
        "import re",
        "import os",
        "def func_1():",
        "return 1",
        ""
    ]
    expected = """import re
import os
def func_1():
    return 1

"""
    codebuilder = tinytemplate.CodeBuilder()
    codebuilder.add_line(code_line[0])
    codebuilder.add_line(code_line[1])
    codebuilder.add_line(code_line[2])
    codebuilder.indent()
    codebuilder.add_line(code_line[3])
    codebuilder.dedent()
    codebuilder.add_line(code_line[4])
    assert str(codebuilder) == expected


def test_compiler_get_globals():
    codebuilder = tinytemplate.CodeBuilder()
    for code in codesource.split('\n'):
        codebuilder.add_line(code)
    g = codebuilder.get_globals()
    print(g)
    assert 'var1' in g and g['var1'] == 123
    assert 'func_1' in g
    assert 'var_str' in g and g['var_str'] == 'unittest'


def test_builder_add_section():
    code = tinytemplate.CodeBuilder()

    code.add_line("def render_function(context, do_dots):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("result = []")
    code.add_line("append_result = result.append")
    code.add_line("extend_result = result.extend")
    code.add_line("to_str = str")

    vars_code.add_line('user_name="abc"')

    print(vars_code)
    print('---')
    print(code)
