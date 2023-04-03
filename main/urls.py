from django.urls import path

from .views import (
    MainView,
    CategoryView,
    PostDetailAndReplyCreate,
    ProfileView,
    ProfileUpdate,
    ProfileDelete,
    ReplyList,
    ReplyApproveView,
    PostCreate,
    logout_user
)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('category/<int:category_id>/', CategoryView.as_view(),
         name='category'),
    path('post/<int:pk>/', PostDetailAndReplyCreate.as_view(), name='post'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit', ProfileUpdate.as_view(), name='profile_edit'),
    path('profile/<int:pk>/delete', ProfileDelete.as_view(),
         name='profile_delete'),
    path('replies/', ReplyList.as_view(), name='replies'),
    path('post/<int:pk>/reply/<int:reply_pk>/', ReplyApproveView.as_view(),
         name='reply'),
    path('post/editor/', PostCreate.as_view(), name='new_post'),
    path('logout/', logout_user, name='logout')
]