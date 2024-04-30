from django.contrib import admin

from .models import Article, Comment

# Модельки для их добавления на админ панель
admin.site.register(Article)
admin.site.register(Comment)