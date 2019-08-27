# tiny-template
Learning Project: A tiny template engine in Python

# Purpose

This is a project written for learning `template-engine` in [500lines](https://github.com/aosabook/500lines/blob/master/template-engine/template-engine.markdown) using Python3.x

# Scope

The core idea is to translate the template language into Python3 code and evaluate the code to generate the final output.

The supported template language is a nano subset of Django according to `500lines`.

For this project, we support following snippet of templating and that's all.

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

And to generate the output, we would call the render function like the following:
```python
templ = "/path/to/template/file.html"

output = render(templ, user_name, product_list)
```
