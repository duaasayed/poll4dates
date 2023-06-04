from django import template
from datetime import datetime
from django.core import serializers
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='split')
def split(value, key):
    return value.split(key)


@register.filter(name='str_date')
def str_date(value, key):
    return datetime.strptime(value, key)


@register.filter(name='queryset_as_json')
def queryset_as_json(qs):
    json_data = serializers.serialize("json", qs)
    return mark_safe(json_data)
