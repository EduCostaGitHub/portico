from typing import Any

from blog.models import Page, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

POST_PER_PAGE = 2

# Create your views here.


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = POST_PER_PAGE
    queryset = Post.objects.get_published()  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context = {}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update(
            {
                'author_pk': author_pk,
                'user': user,
            }
        )

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['author_pk'])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self._temp_context['user']

        user_full_name = user.username

        if (user.first_name):
            user_full_name = f'{user.first_name} {user.last_name}'

        page_title = user_full_name + ' posts - '

        context.update({
            'page_title': page_title,
        })

        return context


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_title = f'{self.object_list[0].category.name} - '  # type: ignore

        context.update({
            'page_title': page_title,
        })

        return context


class TagListView(PostListView):

    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')

        title = self.object_list[0].tags.filter(slug=slug).first().name

        page_title = f'{title} - '

        context.update({
            'page_title': page_title,
        })

        return context


class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(title__icontains=self._search_value) |
            Q(excerpt__icontains=self._search_value) |
            Q(content__icontains=self._search_value)
        )[0:POST_PER_PAGE]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_title = f'{self._search_value[:20]} - '

        context.update({
            'search_value': self._search_value,
            'page_title': page_title,
        })

        return context

    def get(self, request, *args: Any, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()

        page_title = f'{page.title} - '       # type: ignore

        context.update({
            'page_title': page_title,
        })

        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        post_title = f'{post.title} - '       # type: ignore

        context.update({
            'page_title': post_title,
        })

        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
        )
