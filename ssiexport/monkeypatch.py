# coding: utf-8

from django.test.utils import instrumented_test_render


def apply_monkeypatch():
    from django.conf import settings
    settings.STATIC_URL = "http://127.0.0.1:8666" + settings.STATIC_URL
    settings.MEDIA_URL = "http://127.0.0.1:8666" + settings.MEDIA_URL
    from django.template import Template
    Template._render = instrumented_test_render
    return True
