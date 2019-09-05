import tinytemplate


def test_template_s_tokenize_templ():
    template_file = './templates/templ_var_eval.html'
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ._tokenize_templ()
    print(output)
    assert "{{ user_name }}" in output and isinstance(output, list)


def test_template_variable_evaluation_compiler():
    template_file = './templates/templ_var_eval.html'
    # user_name = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.compiler()
    output_str = ''.join(str(s) for s in output.code)
    print()
    print(output_str)
    print()
    # assert user_name in output


def test_template_variable_evaluation_render():
    template_file = './templates/templ_var_eval.html'
    context = dict()
    context['user_name'] = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.render(context)
    print()
    print(output)
    print()
