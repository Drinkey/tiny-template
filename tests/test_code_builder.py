import compiler
import pytest


@pytest.fixture(scope="function", autouse=True)
def setup_function():
    pass

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
    codebuilder = compiler.CodeBuilder()
    codebuilder.add_line(code_line[0])
    codebuilder.add_line(code_line[1])
    codebuilder.add_line(code_line[2])
    codebuilder.indent()
    codebuilder.add_line(code_line[3])
    codebuilder.dedent()
    codebuilder.add_line(code_line[4])
    assert str(codebuilder) == expected

