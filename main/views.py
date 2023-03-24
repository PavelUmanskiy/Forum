from django.shortcuts import render
from django.views.generic import ListView, DetailView

from main.models import (Post, Reply, Category, User)


class MainView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.queryset = Post.objects.all()\
            .select_related('categories', 'author')
        return super().get_queryset()


class CategoryView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.queryset = Post.objects\
            .filter(categories__id=self.kwargs['category_id'])\
                .select_related('categories', 'author')
        return super().get_queryset()


class PostView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        self.queryset = Post.objects\
            .filter(pk=self.kwargs['post_id'])\
                .select_related('categories', 'author')
        return super().get_queryset()


class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'
        