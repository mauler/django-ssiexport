# coding: utf-8

from distutils.dir_util import mkpath
from os.path import join

from django.template.base import TextNode
from django.test.utils import instrumented_test_render

from ssiexport import world


def apply_monkeypatch():
    from django.template import Template
    Template._render = instrumented_test_render
    return

    from django.template.loader_tags import register
    from django.template import loader_tags

    @register.tag("extends")
    def do_extends(parser, token):
        node = loader_tags.do_extends(parser, token)
        print 'extends', node
        print node.nodelist
        print node.parent_name
        print node.template_dirs
        print node.blocks
        return node

    @register.tag("block")
    def do_block(parser, token):
        node = loader_tags.do_block(parser, token)
        print 'parent', node.parent
        path = join(world.path, 'blocks')
        mkpath(path)
        shtml = join(path, '%s.shtml' % node.name)

        _render = node.render

        def render(context):
            rendered = _render(context)
            open(shtml, 'w').write(rendered)
            ssipath = join('../blocks', '%s.shtml' % node.name)
            ssinode = TextNode('<!--#include file="%s" -->' % ssipath)
            return ssinode.render(context)

        node.render = render

        return node
