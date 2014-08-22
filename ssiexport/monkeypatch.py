# coding: utf-8

from django.test.utils import instrumented_test_render


def apply_monkeypatch():
    from django.template import Template
    Template._render = instrumented_test_render
    return True
