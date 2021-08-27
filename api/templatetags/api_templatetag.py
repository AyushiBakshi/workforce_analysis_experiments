from django import template
register = template.Library()
import datetime

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(expects_localtime=True)
def parse_iso(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")