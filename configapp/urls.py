from django.urls import path
from .views import *


urlpatterns = [
    path("", index, name="index"),
    path("posts/<int:pk>/", post_detail, name="post_detail"),

    # path("login/", login_view, name="login"),
    # path("logout/", logout_view, name="logout"),
    # path("register/", register_view, name="register"),
    #
    # path("profile/", profile_view, name="profile_view"),
    # path("profile/edit/", profile_edit, name="profile_edit"),
    #
    # path("posts/<int:pk>/comments/add/", comment_add, name="comment_add"),

    path("posts/", post_list, name="posts"),

    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    path("posts/<int:pk>/comments/", CommentListView.as_view(), name="comment_list"),
    path("posts/<int:pk>/comments/add/", CommentCreateView.as_view(), name="comment_create"),

    path("install/", install, name="install"),

]
# urlpatterns = [
#     # Postlar
#     path("", views.post_list, name="post_list"),
#     path("posts/<int:pk>/", views.post_detail, name="post_detail"),
#
#     # Auth (login / logout / register)
#     path("login/", views.login_view, name="login"),
#     path("logout/", views.logout_view, name="logout"),
#     path("register/", views.register_view, name="register"),
#
#     # Profile
#     path("profile/", views.profile_view, name="profile_view"),
#     path("profile/edit/", views.profile_edit, name="profile_edit"),
#
#     # Comment qo‘shish
#     path("posts/<int:pk>/comments/add/", views.comment_add, name="comment_add"),