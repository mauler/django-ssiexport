# coding: utf-8

from django.db.models.query import QuerySet
from django.test.utils import instrumented_test_render


CALLS = "_monkeypatch_calls"

INVALID = (
    "get_queryset",
    "model",
    # "values_list",
    # "aggregate",
    # "values",
    # "using",
    # "reverse",
)


def patch(original):
    for name in dir(original):

        if name in INVALID:
            continue

        if name.startswith("_"):
            continue

        attr = getattr(original, name)

        if callable(attr):

            def patch_callable(name, func):

                def newfunc(*args, **kwargs):
                    # print 'name', repr(name)
                    result = func(*args, **kwargs)

                    if isinstance(result, QuerySet):
                        if not hasattr(result, CALLS):
                            calls = getattr(original, CALLS, [])
                            setattr(result, CALLS, calls)
                            getattr(result, CALLS).append((name, args, kwargs))
                        patch(result)

                    return result

                setattr(original, name, newfunc)

            patch_callable(name, attr)


def apply_manager_monkeypatch(manager):
    patch(manager)


def apply_monkeypatch():
    from django.conf import settings
    settings.STATIC_URL = "http://127.0.0.1:8666" + settings.STATIC_URL
    settings.MEDIA_URL = "http://127.0.0.1:8666" + settings.MEDIA_URL
    from django.template import Template
    Template._render = instrumented_test_render
    return True
