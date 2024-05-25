# локальные url для приложения
from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('about/', views.about, name='about'),  # создание url
    path('', views.ArticlesListView.as_view(), name='index'),
    path('tag/<slug:tag_slug>/', views.index, name='index_by_tag'),
    path('<int:article_id>/like/', views.like_article, name='like_article'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:article_id>/edit', views.edit, name='edit'),
    path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'),
    path('my_articles', views.my_articles, name='my_articles'),
    path('delete_article/<int:article_id>', views.delete, name='delete'),
    path('add_page/', views.add_page, name='add_page'),
    path('accounts/register/', views.register, name='register'),
    path('search/', views.search, name='search'),

]
