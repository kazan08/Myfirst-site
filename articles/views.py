# этот файл отвечает за то что отображается на сайте
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.urls import reverse

from .models import Article

from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, AddPageForm

def index(request):
    latest_article_list = Article.objects.order_by('-pub_date')[:5]
    username = request.user.username
    return render(request, "articles/list.html", {'latest_articles_list': latest_article_list, 'title': 'Последние статьи', 'usernamne': username} )

def all_a(request):
    latest_article_list = Article.objects.order_by('-pub_date')
    username = request.user.username
    return render(request, "articles/list.html", {'latest_articles_list': latest_article_list, "title": "Все статьи" , 'username': username}, )

#функция detail отвечает за текст статьи, название, и комментарии
def detail(request, article_id):
    try:
        a = Article.objects.get( id = article_id ) # получение id статьи
    except:
        raise Http404("Статья не найдена!")# ошибка 404
    
    latest_comments_list = a.comment_set.order_by("-id")# отображение комментариев

    return render(request, 'articles/detail.html', {'article': a, 'latest_comments_list': latest_comments_list, },)

# создание комментариев
@login_required
def leave_comment(request, article_id):
    try:
        a = Article.objects.get( id = article_id )
    except:
        raise Http404("Статья не найдена!")
    
    # создание комментария
    a.comment_set.create(author_name = request.user, comment_text= request.POST['text'])

    # обновление страницы
    return HttpResponseRedirect( reverse('articles:detail', args = (a.id,)) )

@login_required
def add_page(request):
    if request.method == "POST":
        form = AddPageForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_name = request.user
            article.pub_date = timezone.now()
            article.save()
            return HttpResponseRedirect( reverse('articles:detail', args= (article.id,)) )
    else:
        form = AddPageForm()
    return render(request, "articles/article.html", {'form': form, })

def about(request):
    return render(request, "articles/about.html", )

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit= False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form,})

def edit(request, article_id):
    a = Article.objects.get( id = article_id )
    article = get_object_or_404(Article, pk=a.id)
    if request.method == "POST":
        form = AddPageForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_name = request.user
            article.published_date = timezone.now()
            article.save()
            return HttpResponseRedirect( reverse('articles:detail', args = (a.id,)) )
    else:
        form = AddPageForm(instance=article)
    return render(request, 'articles/article.html', {'form': form})

@login_required
def my_articles(request):
    my_articles = Article.objects.filter( author_name = request.user ).order_by("-pub_date")    
    return render(request, 'articles/my_articles.html', {'my_articles': my_articles})

