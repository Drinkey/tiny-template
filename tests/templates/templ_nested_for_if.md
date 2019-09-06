# {{article.title|upper}}

> {{article.author}}

{% for section in article.sections %}
## {{section.title}}

{{section.content}}
{% if section.has_bullets %}
{% for bullet in section.bullets %}
- {{bullet.item|strip|raw}}
{% endfor %}
{% endif %}
{% endfor %}