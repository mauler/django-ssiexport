# coding: utf-8

from django import template

from classytags.arguments import MultiValueArgument
from classytags.core import Tag, Options

from ssiexport import world


register = template.Library()


class Watch(Tag):
    name = 'watch'
    options = Options(
        MultiValueArgument('objects', required=True, resolve=True),
    )

    def render_tag(self, context, objects):
        if hasattr(world, "watch"):
            world.watch += objects
        return ""


register.tag(Watch)
