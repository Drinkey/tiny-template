import pytest
import tinytemplate

def test_template_s_tokenize_templ():
    template_file = './templates/templ_var_eval.html'
    user_name = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate()
    output = templ._tokenize_templ(template_file)
    print(output)
    assert "{{ user_name }}" in output and isinstance(output, list)

def test_template_variable_evaluation():
    template_file = './templates/templ_var_eval.html'
    user_name = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate()
    output = templ.render(template_file, user_name)
    print(output)
    assert user_name in output
