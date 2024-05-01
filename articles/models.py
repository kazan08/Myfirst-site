import datetime
from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

# Модель статьи
class Article(models.Model):
    author_name = models.ForeignKey(User, on_delete= models.CASCADE)
    article_title = models.CharField('Название Статьи', max_length = 200) # Название статьи
    article_text = models.TextField('Текст статьи') # текст статьи
    pub_date = models.DateTimeField('Publicate date') # дата публикации

    def __str__(self):
        return self.article_title

    # функция показывающая новая ли статья
    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))

    #Перевод на русский
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

# Модель комментария
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    author_name = models.ForeignKey(User, on_delete = models.CASCADE) # автор комментария
    comment_text = models.CharField('Comment text', max_length = 200) # текст комментария
    
    def __str__(self):
        return self.author_name.username

    #Перевод на русский
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'