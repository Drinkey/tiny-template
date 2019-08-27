import re

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
        return "".join(s for s in self.code)

    def add_line(self, line):
        """ add one line of code with indentation"""
        self.code.extend([" " * self._indent_level, line, "\n"])

    def add_section(self, codeblock):
        pass
