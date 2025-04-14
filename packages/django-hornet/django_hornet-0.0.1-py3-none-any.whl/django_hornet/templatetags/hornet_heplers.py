from django import template
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse

from hornet.manager import ComponentManager

register = template.Library()


@register.simple_tag(takes_context=True)
def load_component(context, app_name, component_name):
    request = context["request"]
    manager = ComponentManager(request)
    component = manager.load_component(component_name)
    state = component.__dict__
    html = render_to_string(f"components/{component_name}.html", state)
    return html
