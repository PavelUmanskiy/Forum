from django.urls import path

from .views import (
    MainView,
    CategoryView,
    PostDetailAndReplyCreate,
    ProfileView,
)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('category/<int:category_id>/', CategoryView.as_view(),
         name='category'),
    path('post/<int:pk>/', PostDetailAndReplyCreate.as_view(), name='post'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]