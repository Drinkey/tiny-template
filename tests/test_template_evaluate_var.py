import pytest
import tinytemplate

def test_template_s_tokenize_templ():
    template_file = './templates/templ_var_eval.html'
    user_name = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ._tokenize_templ()
    print(output)
    assert "{{ user_name }}" in output and isinstance(output, list)

def test_template_variable_evaluation():
    template_file = './templates/templ_var_eval.html'
    user_name = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.compiler()
    print()
    print(''.join(str(s) for s in output))
    # assert user_name in output
