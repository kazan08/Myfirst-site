import datetime
from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Article.Status.PUBLISHED)
# Модель статьи
class Article(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликован'

    author_name = models.ForeignKey(User, on_delete= models.CASCADE)# Автор статьи
    article_title = models.CharField('Название Статьи', max_length = 200) # Название статьи
    article_text = models.TextField('Текст статьи') # текст статьи
    pub_date = models.DateTimeField('Дата публикации', default=timezone.now()) # дата публикации
    update = models.DateTimeField('Дата обновления', default=timezone.now()) # дата обновления статьи
    status = models.CharField(verbose_name='Статус',max_length=2, choices=Status.choices, default=Status.DRAFT) # статус статьи
    likes = models.ManyToManyField(User,'лайки', blank=True) # лайки статьи

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    def __str__(self): # Функция чтобы мы видели название статьи в админ панели
        return self.article_title

    # функция показывающая новая ли статья
    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))

    #Перевод на русский
    class Meta:
        ordering = ['-pub_date']
        indexes = [models.Index(fields=['-pub_date'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def get_absolute_url(self):
        return reverse('articles:detail', args=[self.id])

# Модель комментария
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE) # статьия к которой сделан коммент
    author_name = models.ForeignKey(User, on_delete = models.CASCADE) # автор комментария
    comment_text = models.CharField('Текст комментария', max_length = 200) # текст комментария
    created = models.DateTimeField("Создано", default=timezone.now()) # дата создания комментария
    
    def __str__(self): # функция чтобы показывало автора комментария в админ панели
        return self.author_name.username

    #Перевод на русский
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
