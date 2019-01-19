from django import template
from django.conf import settings
import os
import re
import json

from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='get_pid')
def file_exists(string):
	return re.findall(r'\d+', string)[0]


@register.filter(name='tojs')
def js(obj):
    return json.dumps(obj)
