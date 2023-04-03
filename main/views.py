from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy

from SF_FINAL.settings import DEFAULT_FROM_EMAIL

from .models import (Post, Reply, Category, User)
from .forms import (PostForm, ReplyForm, UserForm, ReplyApproveForm)
from .utils import UserIsOwnerOfProfileMixin

class MainView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 5
    
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
    template_name = 'forms/post_n_reply.html'
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
    
    def post(self, request, *args, **kwargs):
        link = reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})
        subject = 'Доброго Вам дня! Кажется под Вашим постом новый отклик!'
        message = f'{self.request.user.username} оставил Вам отклик!'
        html_attachement =  f'<a href="{link}">Посмотреть здесь!</a>'
        recipient = [Post.objects.filter(pk=self.kwargs['pk'])\
            .select_related('author').only('author__email')[0].author.email]
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient,
            from_email=DEFAULT_FROM_EMAIL,
            html_message=html_attachement,
            fail_silently=True
        )
        return super().post(request, *args, **kwargs)


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'forms/post.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('post', kwargs={'pk': self.object.id})
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    
class ProfileUpdate(UserIsOwnerOfProfileMixin, UpdateView):
    form_class = UserForm
    template_name = 'forms/profile_update.html'
    
    def get_object(self, **kwargs):
        return User.objects.get(pk=self.request.user.id)


class ProfileDelete(UserIsOwnerOfProfileMixin, DeleteView):
    template_name = 'forms/profile_delete.html'
    queryset = User.objects.all()
    success_url = reverse_lazy('main')


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'replies.html'
    context_object_name = 'replies'
    
    def get_queryset(self):
        self.queryset = Reply.objects\
            .filter(post__author_id=self.request.user.id, approved=False)\
                .select_related('post', 'author')
        return super().get_queryset()
    


class ReplyApproveView(UpdateView):
    form_class = ReplyApproveForm
    template_name = 'forms/reply.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})
    
    def get_object(self, **kwargs):
        my_obj = Reply.objects.filter(
            approved=False,
            id=self.kwargs['reply_pk']
        ).select_related('author').defer(
                'author__password',
                'author__last_login',
                'author__is_superuser',
                'author__email',
                'author__is_staff',
                'author__is_active',
                'author__date_joined',
                'post',
        )[0]
        return my_obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.filter(pk=self.kwargs['pk'])\
            .prefetch_related('categories').defer('author')[0]
        return context
    
    def post(self, request, *args, **kwargs):
        link = reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})
        subject = 'Доброго Вам дня! Кажется автор одобрил Ваш отклик!'
        message = f'{self.request.user.username} одобрил Ваш отклик!'
        html_attachement = f'<a href="{link}">Посмотреть здесь!</a>'
        recipient = [Reply.objects.filter(pk=self.kwargs['reply_pk'])\
            .select_related('author').only('author__email')[0].author.email]
        print(recipient)
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient,
            from_email=DEFAULT_FROM_EMAIL,
            html_message=html_attachement,
            fail_silently=True
        )
        return super().post(request, *args, **kwargs)


def logout_user(request):
    logout(request)
    return redirect('main')