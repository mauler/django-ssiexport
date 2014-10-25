# coding: utf-8

from datetime import datetime

from django.db import models


class ArticleManager(models.Manager):
    def published(self):
        now = datetime.now()
        qs = super(ArticleManager, self).filter(date_created__lte=now)
        return qs
