from django import template
from django.conf import settings
import os

register = template.Library()

@register.filter(name='file_exists')
def file_exists(filepath):
    path = os.path.join(settings.BASE_DIR, filepath) + '.jpg'
    print(path)
    if os.path.isfile(path):
        return '/'+filepath + '.jpg'
    else:
        return "http://placehold.it/150x150?text=Collection"
