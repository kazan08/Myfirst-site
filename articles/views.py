# этот файл отвечает за то что отображается на сайте
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Count

from taggit.models import Tag

from .models import Article

from .forms import UserRegistrationForm, AddPageForm, SearchForm


def index(request, tag_slug=None):
    latest_article = Article.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        latest_article = latest_article.filter(tags__in=[tag])
    # Постраничная разбивка с 5 постами на страницу
    paginator = Paginator(latest_article, 5)
    page_number = request.GET.get('page', 1)
    try:
        latest_article_list = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        latest_article_list = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу результатов
        latest_article_list = paginator.page(paginator.num_pages)
    return render(request,
                  'articles/list.html',
                  {
                      'latest_articles_list': latest_article_list,
                      'tag': tag
                  }
                  )


# Этот класс отвечает за показ статей
class ArticlesListView(ListView):
    queryset = Article.published.all()
    context_object_name = 'latest_articles_list'
    paginate_by = 5
    template_name = "articles/list.html"


# функция detail отвечает за текст статьи, название, и комментарии
def detail(request, article_id):
    try:
        a = Article.objects.get(id=article_id)  # получение id статьи
    except:
        raise Http404("Статья не найдена!")  # ошибка 404

    post_tags_ids = a.tags.values_list('id', flat=True)
    similar_posts = Article.published.filter(tags__in=post_tags_ids) \
        .exclude(id=article_id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-pub_date')[:4]

    latest_comments_list = a.comment_set.all()  # отображение комментариев

    return render(request,
                  'articles/detail.html',
                  {'article': a,
                   'latest_comments_list': latest_comments_list,
                   'similar_posts': similar_posts,
                   },
                  )


# создание комментариев
@login_required
def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except:
        raise Http404("Статья не найдена!")

    # создание комментария
    a.comment_set.create(author_name=request.user, comment_text=request.POST['text'])

    # обновление страницы
    return HttpResponseRedirect(Article.get_absolute_url(self=a))


@login_required
def add_page(request):
    if request.method == "POST":
        form = AddPageForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_name = request.user
            article.pub_date = timezone.now()
            article.update = timezone.now()
            article.save()
            form.save_m2m()
            return HttpResponseRedirect(Article.get_absolute_url(self=article))
    else:
        form = AddPageForm()
    return render(request, "articles/article.html", {'form': form, })


def about(request):
    return render(request, "articles/about.html", )


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создание нового пользователя по форме
            new_user = user_form.save(commit=False)
            # Ставит пароль который вписал
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняет ысе вписанные данные в базу данных
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form, })


def edit(request, article_id):
    a = Article.objects.get(id=article_id)
    article = get_object_or_404(Article, pk=a.id)
    if request.method == "POST":
        form = AddPageForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_name = request.user
            article.update = timezone.now()
            article.save()
            form.save_m2m()
            return HttpResponseRedirect(Article.get_absolute_url(self=a))
    else:
        form = AddPageForm(instance=article)
    return render(request, 'articles/article.html', {'form': form})


@login_required
def my_articles(request):
    my_articles = Article.objects.filter(author_name=request.user).order_by("-pub_date")
    return render(request, 'articles/my_articles.html', {'my_articles': my_articles})


@login_required()
def delete(request, article_id):
    if request.method == "POST":
        Article.objects.get(id=article_id).delete()
        return HttpResponseRedirect(reverse('articles:my_articles'))


@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('articles:detail', article_id=article.id)


def search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Article.published.annotate(
            similarity=TrigramSimilarity('article_title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,
                  'articles/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
