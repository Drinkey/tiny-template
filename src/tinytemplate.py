"""Covert Template to Python Code
"""

from . import compiler

class TinyTemplate:
    def __init__(self):
        self.code = compiler.CodeBuilder()