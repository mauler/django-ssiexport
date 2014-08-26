# coding: utf-8

from django.db.models.query import QuerySet
from django.test.utils import instrumented_test_render


CALLS = "_monkeypatch_calls"


def apply_manager_monkeypatch(manager):

    def is_valid_name(name):
        return \
            not name.startswith("_") and \
            name not in ("get_query_set", "model", )

    def patch(obj):
        for name in dir(manager):
            attr = getattr(manager, name)

            if not is_valid_name(name):
                continue

            if callable(attr):

                def patch_callable(obj, name, attr):
                    def newobj(*args, **kwargs):
                        result = attr(*args, **kwargs)
                        if isinstance(result, QuerySet):
                            setattr(result, CALLS, getattr(obj, CALLS, []))
                            getattr(result, CALLS).append((name, args, kwargs))
                            patch(result)
                        return result
                    setattr(obj, name, newobj)

                patch_callable(obj, name, attr)

    patch(manager)


def apply_monkeypatch():
    from django.conf import settings
    settings.STATIC_URL = "http://127.0.0.1:8666" + settings.STATIC_URL
    settings.MEDIA_URL = "http://127.0.0.1:8666" + settings.MEDIA_URL
    from django.template import Template
    Template._render = instrumented_test_render
    return True
