from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from .forms import ArticleForm
from .models import Article


# Create your views here.
class DashboardView(ListView):
    template_name = 'kbase/dashboard.html'
    model = Article
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        queryset = Article.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
            return queryset
        else:
            sort = self.request.GET.get('sort_latest', '-modified_date')
            return queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search')
        if search_query:
            context['search'] = search_query
        return context


class NewArticleView(CreateView):
    template_name = 'kbase/new-edit.html'
    form_class = ArticleForm
    model = Article

    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy(viewname='article', kwargs={'slug': slug})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ArticleView(DetailView):
    template_name = 'kbase/article.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        user = self.request.user
        can_edit = article.can_user_edit(user)
        context['can_edit'] = can_edit
        return context


class EditArticleView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'kbase/new-edit.html'

    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy(viewname='article', kwargs={'slug': slug})

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if not article.can_user_edit(request.user):
            # raise PermissionDenied #Return 403 #TODO Think about 403 or 302
            return redirect(reverse_lazy(viewname='article', kwargs={'slug': article.slug}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_mode'] = True
        return context
