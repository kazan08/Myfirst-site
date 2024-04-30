# этот файл отвечает за то что отображается на сайте
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from django.urls import reverse

from .models import Article

from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm

menu = [
    {'title': 'Все статьи', 'url_name':'articles:all_a'},
    {'title': 'О сайте', 'url_name': 'articles:about'},
    {'title': 'добавить статью', 'url_name': 'articles:add_page'},
    {'title': 'Обратня свазь', 'url_name': 'articles:contact'},
]

def index(request):
    latest_article_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, "articles/list.html", {'latest_articles_list': latest_article_list, 'menu':menu},)

def all_a(request):
    latest_article_list = Article.objects.order_by('-pub_date')
    return render(request, "articles/list.html", {'latest_articles_list': latest_article_list, 'menu':menu},)

#функция detail отвечает за текст статьи, название, и комментарии
def detail(request, article_id):
    try:
        a = Article.objects.get( id = article_id ) # получение id статьи
    except:
        raise Http404("Статья не найдена!")# ошибка 404
    
    latest_comments_list = a.comment_set.order_by("-id")# отображение комментариев

    return render(request, 'articles/detail.html', {'article': a, 'latest_comments_list': latest_comments_list, 'menu': menu},)

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
    return render(request, 'articles/article.html', {'menu': menu})

@login_required
def leave_article(request):
    Article.objects.create(author_name= request.user,article_title = request.POST['title'], article_text= request.POST['text'], pub_date = request.POST['datetime'])

    return HttpResponseRedirect( reverse('articles:index') )


def about(request):
    return render(request, "articles/about.html", {'menu':menu})

def contact(request):
    return HttpResponse("Вы не сможете связатся")

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'menu': menu})
