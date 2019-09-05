# tiny-template
Learning Project: A tiny template engine in Python

# Purpose

This is a project written for learning `template-engine` in [500lines](https://github.com/aosabook/500lines/blob/master/template-engine/template-engine.markdown) using Python3.x

# Scope

The core idea is to translate the template language into Python3 code and evaluate the code to generate the final output.

The supported template language is a nano subset of Django according to `500lines`.

For this project, we support following syntax:

- variable property accessing with dot, e.g. `var.property`
- loops: `{{% for var in iterable %}} ... {{% endfor %}}`
- condition: `{{% if var %}} ... {{% endif %}}`
- comment: `{# this is comment and will not be evaluated #}`
- function call: `var|function_call` (only one parameter)

A snippet of the template

```html
<p>Welcome, {{user_name}}!</p>
<p>Products:</p>
<ul>
{% for product in product_list %}
    {% if product.name|exists %}
    <li>{{ product.name }}:{{ product.price|format_price }}</li>
    {% endif %}
{% endfor %}
</ul>
```
> The snippet may not reasonable but shows the general ideas.

And to generate the output, we would call the render function like the following:
```python
templ = "/path/to/template/file.html"

output = render(templ, user_name, product_list)
```

# Plan

0. `[DONE]` PoC, try to understand the concept with simple code
1. `[DONE]` Support variable evaluation with out dots
2. `[DONE]` Support variable evaluation with one or two dots
3. `[DONE]` Support `if` statement
4. **[TODO]** Support `for` statement
5. **[TODO]** Support nested `for` and `if` statements
6. **[TODO]** Support filters with pipes, multiple pipes
7. **[TODO]** Refactoring all codes

# Principles

Write test first, develop code later
