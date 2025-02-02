from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='star_rating')
def star_rating(value):
    stars_html = ""
    for i in range(5):
        if i < int(value):
            stars_html += "<span class='fa-star checked'></span>"
        else:
            stars_html += "<span class='fa-star'></span>"
    return mark_safe(stars_html)


@register.filter(name='model_type')
def model_type(value):
    return type(value).__name__


register.filter("star_rating", star_rating)
register.filter("model_type", model_type)
