import pathlib
import tinytemplate


TEMPLATE_DIR = pathlib.Path(__file__).resolve().parent

def test_template_s_tokenize_templ():
    template_file = f'{str(TEMPLATE_DIR)}/templates/templ_var_eval.html'
    templ = tinytemplate.parse_template_file(template_file)
    print(templ)
    assert "{{ user_name }}" in templ and isinstance(templ, list)


def test_template_variable_evaluation_compiler():
    template_file = f'{str(TEMPLATE_DIR)}/templates/templ_var_eval.html'
    # user_name = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ._compile_to_pycode()
    output_str = ''.join(str(s) for s in output.code)
    print()
    print(output_str)
    print()
    # var name in template file should be resolve as new name with c_ prefix
    assert "c_user_name" in output_str and "c_user_name =" in output_str


def test_template_variable_evaluation_render():
    template_file = f'{str(TEMPLATE_DIR)}/templates/templ_var_eval.html'
    context = dict()
    context['user_name'] = "Junkai Zhang"
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.render(context)
    print()
    print(output)
    print()
    assert "Junkai Zhang" in output

def test_template_access_properties_with_dots():
    template_file = f'{str(TEMPLATE_DIR)}/templates/templ_props.html'
    context = {
        'user':{
            'name': 'Clark Kent',
            'role': 'Justice Leaguage',
            'alias': 'Super Man'
        }
    }
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.render(context)
    print()
    print(output)
    print()
    for val in context['user'].values():
        assert val in output

def test_template_access_properties_with_dots_two_dots():
    template_file = f'{str(TEMPLATE_DIR)}/templates/templ_two_dots_props.html'
    context = {
        'user':{
            'name': 'Clark Kent',
            'role': 'Justice Leaguage',
            'alias': 'Super Man',
            'tags': {
                'keyword': '#fly,#steel,#hero'
            }
        }
    }
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.render(context)
    print()
    print(output)
    print()
    assert 'fly' in output

def test_template_if_statement():
    template_file = f'{str(TEMPLATE_DIR)}/templates/templ_if.html'
    context = {
        'user':{
            'name': 'Clark Kent',
            'role': 'Justice Leaguage',
            'alias': 'Super Man',
            'is_logged_in': False
        }
    }
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.render(context)
    print()
    print(output)
    print()
    assert 'Justice Leaguage' not in output

def test_template_for_statement():
    template_file = f'{str(TEMPLATE_DIR)}/templates/templ_for.html'
    context = {
        'user':{
            'name': 'Clark Kent',
            'role': 'Justice Leaguage',
            'alias': 'Super Man',
            'is_logged_in': False
        },
        'product_list': [
            {
                'name': "spacecraft",
                'price': 100
            },
            {
                'name': 'fortress',
                'price': 10000
            }
        ]
    }
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.render(context)
    print()
    print(output)
    print()
    assert 'spacecraft' in output
    assert 'fortress' in output
    assert 'Clark Kent' in output

def test_template_nested_for_if_statement():
    template_file = f'{str(TEMPLATE_DIR)}/templates/templ_nested_for_if.md'
    def my_func(s):
        return f"{s}++"
    context = {
        'article': {
            'title': 'Software Engineering',
            'author': 'Copy from Internet',
            'sections': [
                {
                    'title': 'History',
                    'content': "don't know yet",
                    'has_bullets': False,
                },
                {
                    'title': 'Definition',
                    'content': "quote from wiki",
                    'has_bullets': True,
                    'bullets': [
                        {
                            'item': 'use of enginering method'
                        },{
                            'item': 'application of engineering'
                        },{
                            'item': 'what hell i am saying'
                        }
                    ]
                },{
                    'title': 'workflow',
                    'content': 'see the chart',
                    'has_bullets': False,
                }
            ]
        },
        'upper': str.upper,
        'strip': str.strip,
        'raw': my_func
    }
    templ = tinytemplate.TinyTemplate(template_file)
    output = templ.render(context)
    print()
    print(output)
    print()
    assert '++' in output
    assert 'enginering method' in output
    assert '# Software Engineering'.upper() in output
