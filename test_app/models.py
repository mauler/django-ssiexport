# coding: utf-8

from django.db import models

from .manager import ArticleManager


class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name", )

    def __unicode__(self):
        return self.name


class Article(models.Model):
    objects = ArticleManager()
    authors = models.ManyToManyField("Author")
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u"/article/%d/" % self.pk
