# coding: utf-8

from distutils.filelist import findall

from django.test import TestCase

from ssiexport.models import URL
from ssiexport.monkeypatch import apply_monkeypatch
from ssiexport.utils import \
    export_instance, export_url, get_watch_instances, get_exporters, \
    connect_signals

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
        connect_signals()
        article = Article.objects.create(title="new article")
        # from django.db.models import signals
        # signals.post_save.send(sender=type(article), instance=article)
        qs = URL.objects.filter(path=article.get_absolute_url())
        self.assertTrue(qs.exists())
