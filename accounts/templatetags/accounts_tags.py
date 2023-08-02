from django import template

register = template.Library()

@register.filter
def get_val_by_key(d, key):
    return d.get(key)


@register.filter
def get_obj_value(d, key):
    return d.data.get(key)

