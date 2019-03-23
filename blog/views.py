from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from .forms import PostForm, UserForm
from .models import Post, Blog


@login_required
def index(request, **kwargs):
    posts = Post.objects.filter(blog__subscribed__username=request.user.username)
    blogs = Blog.objects.filter(subscribed__username=request.user.username)
    pages = 10
    paginator = Paginator(posts, pages)
    page = request.GET.get('page')
    news = paginator.get_page(page)

    return render(request, 'index.html', {'news': news, 'blogs': blogs})


def readed(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    if (user not in post.readed_user.all()):
        post.readed_user.add(user)

    print()
    return redirect('index')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_add.html'

    def get_form_kwargs(self):
        kwargs = super(PostCreate, self).get_form_kwargs()
        blog = Blog.objects.get(owner=self.request.user)
        kwargs.update({'blog': blog})
        return kwargs

    def form_valid(self, form):
        form.instance.blog = Blog.objects.get(owner=self.request.user)
        return super(PostCreate, self).form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:blog')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(PostDelete, self).get_object()
        if not obj.blog.owner == self.request.user:
            raise Http404
        return obj


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/main.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(blog__owner__username=self.request.user)

        return queryset


def subscribe(request, **kwargs):
    # current subscribe
    blogs = Blog.objects.filter(subscribed=request.user)

    # setting subscribe
    # select = Blog.objects.filter(subscribed=request.user).values_list('owner_id', flat=True)
    select = Blog.objects.filter(subscribed=request.user).prefetch_related('subscribed').values_list('subscribed__blog',
                                                                                                     flat=True)
    form = UserForm(initial={'subscribed': select})
    form.save(commit=False)
    user = request.user
    user.subscribed.clear()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            for k, v in form.cleaned_data.items():
                for i in range(len(v)):
                    user.subscribed.add(v[i])
            return redirect('index')
        else:
            print(form.errors)

    return render(request, 'blog/subscribe.html', {'blogs': blogs, 'form': form})
