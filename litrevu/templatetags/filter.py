from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='star_rating')
def star_rating(value):
    """
    Convert a numerical rating into a series of star icons (max of 5), returning the result as safe HTML.

    :param value: An integer
    :return: An HTML string representing the star rating
    """
    stars_html = ""
    for i in range(5):
        if i < int(value):
            stars_html += "<span class='fa-star checked'></span>"
        else:
            stars_html += "<span class='fa-star'></span>"
    return mark_safe(stars_html)


@register.filter(name='model_type')
def model_type(value):
    """
    Return the class name (model name) of the given value.
    :param value: An instance of a model.
    :return: A string representing the model's class name.
    """
    return type(value).__name__


register.filter("star_rating", star_rating)
register.filter("model_type", model_type)
