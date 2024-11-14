from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def format_image_name(area_name):
    return area_name.lower().replace(' ', '_')