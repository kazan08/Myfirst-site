from django.contrib import admin

from .models import Article, Comment

# Модельки для их добавления на админ панель
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['article_title', 'author_name', 'pub_date', 'status']
    list_filter = ['status', 'pub_date', 'author_name']
    search_fields = ['article_title', 'article_text']
    raw_id_fields = ['author_name']
    date_hierarchy = 'pub_date'
    ordering = ['status', 'pub_date']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name',  'article', 'created',]
    list_filter = ['author_name', 'created']
    search_fields = ['author_name', 'comment_text']
    raw_id_fields = ['author_name', 'article']