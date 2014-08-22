# coding: utf-8

from django.test import TestCase

from ssiexport.utils import export_url, export_instance

from .models import Article, Author


class UtilsTestCase(TestCase):

    def setUp(self):
        self.paulo = Author.objects.create(name="Paulo")
        self.roberto = Author.objects.create(name="Roberto")
        self.article = Article.objects.create(title="My First Post")
        self.article.authors.add(self.paulo)

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

    def test_export_instance(self):
        dburl, dbinstance = export_instance(self.article)
        self.assertQuerysetEqual(
            dburl.templates.all(),
            ['<Template: article.html>', '<Template: index.html>'],
        )
