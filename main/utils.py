from django.contrib.auth.mixins import UserPassesTestMixin
import main.models


# class UserIsAuthorOfPostMixin(UserPassesTestMixin):
#     def test_func(self) -> bool:
#         user_author_id = main.models.Author.objects.get(user__pk=self.request.user.pk).id
#         post_author_id = main.models.Post.objects.get(pk=self.kwargs['pk']).author_id
#         return user_author_id == post_author_id


class UserIsOwnerOfProfileMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        user_id = main.models.User.objects.get(pk=self.request.user.pk).id
        profile_user_id = main.models.User.objects.get(pk=self.kwargs['pk']).id
        return user_id == profile_user_id