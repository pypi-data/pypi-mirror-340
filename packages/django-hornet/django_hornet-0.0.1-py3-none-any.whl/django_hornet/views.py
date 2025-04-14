from django.views.generic import TemplateView
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse

from .manager import ComponentManager


class HornetlView(TemplateView):

    def render_to_component(self, state=None):
        if not state is None:
            self.state = state
        else:
            self.state = self.component.__dict__
        html = render_to_string(f"components/{self.component_name}.html", self.state)
        return render(self.request, self.template_name, {"component_html": html})

    def update_to_component(self):
        self.manager.save_component(self.component_name, self.component)
        html = render_to_string(f"components/{self.component_name}.html", self.state)
        return HttpResponse(html)

    def dispatch(self, *args, **kwargs):
        self.manager = ComponentManager(self.request)
        self.component = self.manager.load_component(self.component_name)
        self.state = self.component.__dict__
        self.html = render_to_string(
            f"components/{self.component_name}.html", self.state
        )
        return super(HornetlView, self).dispatch(*args, **kwargs)
