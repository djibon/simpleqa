from django import template
from django.conf import settings
from django.utils import dateformat
from django.template import Library, Node, resolve_variable, TemplateSyntaxError

from tagging.models import Tag

register = template.Library()
@register.inclusion_tag("core/tags.html")
def show_tags(question):
    tags = Tag.objects.get_for_object(question)
    return {
        'tags':tags
        }
