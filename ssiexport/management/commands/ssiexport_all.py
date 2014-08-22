# coding: utf-8

from distutils.dir_util import mkpath
from os.path import join, dirname
from os import system, symlink

from django.core.management.base import BaseCommand

from ssiexport.monkeypatch import apply_monkeypatch
from ssiexport.utils import export_url, export_instance
from ssiexport import world


world.extends = None


from django.conf import settings


settings.STATIC_URL = "http://127.0.0.1:8666" + settings.STATIC_URL
settings.MEDIA_URL = "http://127.0.0.1:8666" + settings.MEDIA_URL


def lns(dst, src):
    symlink(dst, src)
    # system("rm -v %s" % src)
    # system("ln -vs %s %s" % (dst, src))


class Command(BaseCommand):
    help = u"ssiexport"

    def handle(self, *args, **options):
        apply_monkeypatch()

        urls = [
            '/',
            # '/home2',
            # '/about',
            # '/splash',
        ]

        # Content.objects.all().delete()
        # Content.objects.get_or_create(title="News #1", published=True)
        # Content.objects.get_or_create(title="News #2", published=True)
        # Content.objects.get_or_create(title="News #3", published=False)
        # Content.objects.get_or_create(title="News #4", published=True)
        # Content.objects.get_or_create(title="News #5", published=False)

        # for i in Content.objects.all():
        #     urls.append(i.get_absolute_url())

        from portal.models import Noticia
        for i in Noticia.objects.published()[:5]:
            export_instance(i)

        for url in urls:
            print url
            export_url(url)
            continue
            from django.test.client import Client
            client = Client()
            path = join("export", "www", url[1:])
            world.path = path
            mkpath(path)
            shtml = join(path, 'index.html')
            response = client.get(url, follow=True)
            content = response.content
            templates = [i.name for i in response.templates]
            for template in templates[:1]:
                if url.strip() == '/':
                    base_path = '../../'
                else:
                    base_path = (url.count('/') + 2) * '../'
                template_name = template.replace("html", "shtml")
                path = join(world.path, 'templates', dirname(template_name))
                mkpath(path)
                src = join(world.path, 'templates', template_name)
                dst = join(base_path, 'templates', template_name)
                lns(dst, src)
                path = join('export', 'templates', template_name)
                mkpath(dirname(path))
                open(path, 'w').write(response.content)
                if url.strip() == '/':
                    base_path = '../'
                else:
                    base_path = (url.count('/') + 1) * '../'
                template_path = join(base_path, "templates", template_name)
                # template_path = join("templates", template_name)
                content = '<!--#include file="%s" -->' % template_path
            open(shtml, 'w').write(content)
            # print "=" * 80
            # print response.content
            # print
        print world.watch
        system("tree export")
