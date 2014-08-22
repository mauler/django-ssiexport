from .models import Article


class ArticleExport(object):
    def get_urls(self):
        urls = ['/']
        urls += [i.get_aboslute_url() for i in Article.objects.all()]
        return urls


exporters = (ArticleExport, )
