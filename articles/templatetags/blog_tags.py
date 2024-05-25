from django import template
from ..models import Article
register = template.Library()
@register.simple_tag
def total_posts():
 return Article.published.count()