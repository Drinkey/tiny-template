
def read_template(templ_file):
    content = ''
    with open(templ_file) as fp:
        content = fp.read()
    return content


def do_dot(var, prop):
    try:
        return var.get(prop)
    except KeyError:
        return var[prop]


context = {
    'title': 'Software Engineering',
    'author_name': 'Junkai Zhang',
    'content': [
        {
            'header': 'Definition',
            'content': 'develop a software\n- option 1\n- option 2'
        },
        {
            'header': 'Engineering Method',
            'content': "do a job"
        },
        {
            'header': 'Workflow',
            'content': 'show a chart'
        }
    ],
    'formater': int
}


templ_str = """
# {{title}}

> {{author_name}}

{% for section in content %}

## {{section.header|to_str}}

{{section.content}}
{% endfor %}

"""


def test_variable_evaluation():
    result = list()

    extend_result = result.extend
    append_result = result.append
    to_str = str
    extend_result([
        '# ',
        context['title'],
        '\n\n',
        '> ',
        to_str(context['author_name']),
        '\n\n',
    ])

    for head in context['content']:
        extend_result([
            '## ',
            to_str(do_dot(head, 'header')),
            '\n\n',
            to_str(do_dot(head, 'content')),
            '\n\n'
        ])

    append_result('tags: #software, #engineering, #SDLC')

    result_str = ''.join(result)
    print(result)
    print(result_str)
    assert "Junkai" in result_str
