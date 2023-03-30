from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import (Post, Reply, User)


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ['title', 'content', 'categories']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание поста',
            'categories': 'Категории',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Ваш заголовок',
                'class': 'form-text',
            }),
            'content': forms.CharField(widget=CKEditorWidget())
        }


class ReplyForm(forms.ModelForm):
    class Meta():
        model = Reply
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Ваш отклик',
                'class': 'form-reply',
            }),
        }


class ReplyApproveForm(forms.ModelForm):
    class Meta():
        model = Reply
        fields = ['approved']
        labels = {
            'approved': '',
        }


class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'Юзернейм',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Эл. почта',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Ваш юзернейм',
                'class': 'form-text',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя',
                'class': 'form-text',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Ваша фамилия',
                'class': 'form-text',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ваша эл. почта',
                'class': 'form-text',
            }),
        }