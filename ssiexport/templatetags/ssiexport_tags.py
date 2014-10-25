# coding: utf-8

from django.db.models.query import QuerySet
from django import template

from classytags.arguments import MultiValueArgument
from classytags.core import Tag, Options

from ssiexport.monkeypatch import CALLS
from ssiexport import world


register = template.Library()


class Watch(Tag):
    name = 'watch'
    options = Options(
        MultiValueArgument('objects', required=True, resolve=True),
    )

    def render_tag(self, context, objects):

        if hasattr(world, "watch"):
            for obj in objects:
                if isinstance(obj, QuerySet):
                    if not hasattr(obj, CALLS):
                        msg = "Queryset for model %s is not monkey patched."
                        raise Exception(msg % obj.model)

                world.watch.append(obj)
        return ""


register.tag(Watch)
