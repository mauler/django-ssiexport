from .models import Article


class ArticleExport(object):

    def get_querysets(self):
        return (
            Article.objects.all(),
        )

    def get_urls(self):
        urls = ['/']
        return urls


exporters = (ArticleExport, )
