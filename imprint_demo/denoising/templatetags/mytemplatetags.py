from django import template
from django.conf import settings
import os
import re

register = template.Library()

@register.filter(name='get_pid')
def file_exists(string):
	return re.findall(r'\d+', string)[0]
