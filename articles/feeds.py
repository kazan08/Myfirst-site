import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Article


class LatestPostsFeed(Feed):
    title = 'Блог4'
    link = reverse_lazy('articles:index')
    description = 'Новые статьи'


    def items(self):
        return Article.published.all()[:5]

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):

        return truncatewords_html(markdown.markdown(item.article_text), 30)

    def item_pubdate(self, item):

        return item.pub_date
