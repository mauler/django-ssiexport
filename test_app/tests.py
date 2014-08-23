# coding: utf-8

from distutils.filelist import findall

from django.test import TestCase

from ssiexport.models import URL
from ssiexport.monkeypatch import apply_monkeypatch
from ssiexport.utils import \
    export_instance, export_url, get_watch_instances, get_exporters

from .export import ArticleExport
from .models import Article, Author


class UtilsTestCase(TestCase):

    def setUp(self):
        self.paulo = Author.objects.create(name="Paulo")
        self.roberto = Author.objects.create(name="Roberto")
        self.article = Article.objects.create(title="My First Post")
        self.article.authors.add(self.paulo)

    def test_apply_monkeypatch(self):
        self.assertTrue(apply_monkeypatch())

    def test_export_instance(self):
        dburl, dbinstance = export_instance(self.article)
        self.assertQuerysetEqual(
            dburl.templates.all(),
            ['<Template: article.html>', '<Template: index.html>'],
        )

    def test_export_url(self):
        dburl = export_url("/")
        self.assertQuerysetEqual(
            dburl.templates.all(),
            ['<Template: index.html>'],
        )
        dburl = export_url("/")
        self.assertQuerysetEqual(
            dburl.templates.all(),
            ['<Template: index.html>'],
        )
        self.assertEqual(
            findall("export"),
            ['export/www/index.shtml', 'export/www/article/1/index.shtml'])

    def test_get_exporters(self):
        self.assertEqual(get_exporters(), [ArticleExport])

    def test_get_watch_instances(self):
        from ssiexport import world
        world.watch.append(self.article)
        world.watch.append(Author.objects.all())
        instances = get_watch_instances()
        self.assertEqual(
            [i.content_object for i in instances],
            [self.article, self.paulo, self.roberto]
        )
        self.assertEqual(
            findall("export"),
            ['export/www/index.shtml', 'export/www/article/1/index.shtml'])

    def test_connect_signals(self):
        from ssiexport.utils import connect_signals
        connect_signals()
        from django.db.models.loading import get_model
        from django.db.models import signals
        from ssiexport.models import Instance
        for exporter_class in get_exporters():
            exporter = exporter_class()
            for qs in getattr(exporter, "get_querysets", lambda: [])():

                def post_delete_signal(sender, instance, *args, **kwargs):
                    instance = Instance.get_from_instance(instance)
                    for dburl in instance.instance_url_set.all():
                        dburl.shtml.delete()
                        dburl.delete()

                    for url in instance.url_set.all():
                        export_url(url.path)

                    instance.delete()

                def post_save_signal(sender, instance, *args, **kwargs):
                    if qs.filter(pk=instance.pk).exists():
                        export_instance(instance)

                model_class = get_model(
                    qs.model._meta.app_label, qs.model._meta.module_name)
                signals.post_delete.connect(
                    post_delete_signal, sender=model_class)
                signals.post_save.connect(
                    post_save_signal, sender=model_class)

        article = Article.objects.create(title="new article")
        qs = URL.objects.filter(path=article.get_absolute_url())
        self.assertTrue(qs.exists())
        article.delete()
