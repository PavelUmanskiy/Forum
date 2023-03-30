from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy

from .models import (Post, Reply, Category, User)
from .forms import (PostForm, ReplyForm, UserForm, ReplyApproveForm)

class MainView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.queryset = Post.objects.all()\
            .select_related('author').defer(
                'author__password',
                'author__last_login',
                'author__is_superuser',
                'author__email',
                'author__is_staff',
                'author__is_active',
                'author__date_joined',
            ).prefetch_related('categories')
        return super().get_queryset()


class CategoryView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.queryset = Post.objects\
            .filter(categories__id=self.kwargs['category_id'])\
                .select_related('author').defer(
                'author__password',
                'author__last_login',
                'author__is_superuser',
                'author__email',
                'author__is_staff',
                'author__is_active',
                'author__date_joined',  
                ).prefetch_related('categories')
        return super().get_queryset()


class PostDetailAndReplyCreate(LoginRequiredMixin, CreateView):
    template_name = 'post_n_reply.html'
    form_class = ReplyForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies = Reply.objects.filter(approved=True).select_related('author')\
            .defer(
                'author__password',
                'author__last_login',
                'author__is_superuser',
                'author__email',
                'author__is_staff',
                'author__is_active',
                'author__date_joined',
            )
        context['post'] = Post.objects\
            .filter(pk=self.kwargs['pk'])\
                .select_related('author').defer(
                'author__password',
                'author__last_login',
                'author__is_superuser',
                'author__email',
                'author__is_staff',
                'author__is_active',
                'author__date_joined',
                ).prefetch_related(Prefetch('reply_set', queryset=replies))\
                    .prefetch_related('categories')[0]
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        self.object.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)    


class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'forms/post.html'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    
class ProfileUpdate(UpdateView):
    form_class = UserForm
    template_name = 'forms/profile.html'
    
    def get_object(self, **kwargs):
        return User.objects.get(pk=self.request.user.id)


class ReplyApproveView(UpdateView):
    form_class = ReplyApproveForm
    template_name = 'forms/replies.html'
    
    def get_object(self, kwargs):
        return Reply.objects.filter(
            author__id=self.request.user.id,
            approved=False
        ).select_related('author', 'post').defer(
                'author__password',
                'author__last_login',
                'author__is_superuser',
                'author__email',
                'author__is_staff',
                'author__is_active',
                'author__date_joined',
                
                'post__content',
                'post__categories',
                'post__author',
        )