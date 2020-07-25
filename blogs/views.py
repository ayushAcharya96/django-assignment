from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from django.contrib.auth import get_user_model

USER = get_user_model()

from .forms import PostCreateForm
from .models import Post

# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blogs/home.html', context)

class PostlListView(ListView):
    model = Post
    template_name = 'blogs/home.html'
    context_object_name = 'posts'
    ordering = ['-created_on']
    paginate_by = 4

class UserPostlListView(ListView):
    model = Post
    template_name = 'blogs/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(USER, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_on')

class PostDetailView(DetailView):
    model = Post
    query_pk_and_slug = True

class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = 'blogs/post_form.html'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        # self.request.user.
        # self.send_confirmation_email()
        return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostCreateForm
    slug_url_kwarg = 'slug'
    model = Post
    template_name = 'blogs/post_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.    user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    query_pk_and_slug = True
    success_url = '/blogs/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blogs/about.html', {})