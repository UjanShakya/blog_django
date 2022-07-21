from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Blog, BlogAuthor, BlogComment
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'num_visits': num_visits, }
    return render(request, 'index.html', context)


class BlogListView(ListView):
    model = Blog
    paginate_by = 5


class BlogListByAuthorView(ListView):
    model = Blog
    paginate_by = 5
    template_name = 'base/blog_list_by_author.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk=id)
        return Blog.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        context = super(BlogListByAuthorView, self).get_context_data(**kwargs)
        context['blogger'] = get_object_or_404(
            BlogAuthor, pk=self.kwargs['pk'])
        return context


class BlogDetailView(DetailView):
    model = Blog


class BloggerListView(ListView):
    model = BlogAuthor
    paginate_by = 5


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    model = BlogComment
    fields = ['description']

    def get_context_data(self, **kwargs):
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(
            Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk']})
