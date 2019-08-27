import pytest
import tinytemplate

def test_template_sigle_var_eval():
    template_file = './templates/templ_var_eval.html'
    user_name = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate()
    output = templ.render(template_file, user_name)

    assert f"{user_name}" in output