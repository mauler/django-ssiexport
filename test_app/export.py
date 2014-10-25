from .models import Article, Author


class ArticleExport(object):

    def get_querysets(self):
        return (
            Author.objects.all(),
            Article.objects.all(),
        )

    def get_urls(self):
        urls = ['/']
        return urls


exporters = (ArticleExport, )
