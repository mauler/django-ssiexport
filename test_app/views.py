# coding: utf-8

from django.shortcuts import render, get_object_or_404

from .models import Article


def article(request, pk):
    obj = get_object_or_404(Article, pk=pk)
    return render(request, "article.html", {
        "article": obj,
    })


def index(request):
    return render(request, "index.html", {
        'articles': Article.objects.all(),
    })
