# локальные url для приложения
from django.urls import path 

from . import views

app_name = 'articles'
urlpatterns = [
    path('about/', views.about, name='about'), # создание url
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail, name = 'detail'),
    path('<int:article_id>/leave_comment/', views.leave_comment, name = 'leave_comment'),
    path('all_a/', views.all_a, name='all_a'),
    path('add_page/', views.add_page, name='add_page'),
    path('add_page/leave_article', views.leave_article, name='leave_article'),
    path('contact/', views.contact, name="contact"),
    path('register/', views.register, name='register'),
]