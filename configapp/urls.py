from django.urls import path
from .views import *

urlpatterns = [
    # Home page
    path("", index, name="index"),
    
    # Authentication URLs
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    
    # Profile URLs
    path("profile/", profile_view, name="profile_view"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    
    # Posts URLs (Template-based views)
    path("posts/", post_list, name="post_list"),
    path("posts/<int:pk>/", post_detail, name="post_detail"),
    path("posts/create/", post_create, name="post_create"),
    path("posts/<int:pk>/edit/", post_edit, name="post_edit"),
    path("posts/<int:pk>/delete/", post_delete, name="post_delete"),
    
    # API URLs for Posts (if needed)
    path("api/posts/", PostListView.as_view(), name="api_post_list"),
    path("api/posts/<int:pk>/", PostDetailView.as_view(), name="api_post_detail"),
    path("api/posts/create/", PostCreateView.as_view(), name="api_post_create"),
    path("api/posts/<int:pk>/edit/", PostUpdateView.as_view(), name="api_post_edit"),
    path("api/posts/<int:pk>/delete/", PostDeleteView.as_view(), name="api_post_delete"),
    
    # Comments URLs (API)
    path("api/posts/<int:pk>/comments/", CommentListView.as_view(), name="api_comment_list"),
    path("api/posts/<int:pk>/comments/add/", CommentCreateView.as_view(), name="api_comment_create"),
    
    # Install demo data
    path("install/", install, name="install"),
    
    # Frontend Admin URLs
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),
    path("admin-panel/users/", admin_users, name="admin_users"),
    path("admin-panel/users/<int:user_id>/", admin_user_detail, name="admin_user_detail"),
    path("admin-panel/posts/", admin_posts, name="admin_posts"),
    path("admin-panel/posts/<int:post_id>/delete/", admin_delete_post, name="admin_delete_post"),
    path("admin-panel/comments/", admin_comments, name="admin_comments"),
    path("admin-panel/comments/<int:comment_id>/delete/", admin_delete_comment, name="admin_delete_comment"),
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