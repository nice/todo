from datetime import date, datetime, timedelta
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if pattern in request.path:
        return 'active'
    return ''

@register.simple_tag
def expired(task):
    if task.due_date < date.today() and task.state != 'done':
        return 'expired'

# settings value
# usage: {% settings_value "LANGUAGE_CODE" %}
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")
