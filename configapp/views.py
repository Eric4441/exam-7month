from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment
from .serializers import UserProfileSerializer, PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Profile
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class ProfileEditView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


# Posts
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionError("Siz faqat o'zingizning postingizni o'zgartira olasiz")
        serializer.save()


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError("Siz faqat o'zingizning postingizni o'chira olasiz")
        instance.delete()


# Comments
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["pk"])


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        serializer.save(author=self.request.user, post_id=post_id)


# Install
@api_view(["GET"])
def install(request):
    user = User.objects.create_user(username="demo", password="demo123")
    profile = UserProfile.objects.create(user=user, bio="Demo user")
    post = Post.objects.create(author=user, title="Hello World!", content="This is demo post.")
    Comment.objects.create(post=post, author=user, content="Demo comment")
    return Response({"message": "Demo data created!"})
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/list.html", {"posts": posts})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "auth/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("post_list")
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

# === Profile ===
@login_required
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, "profile/view.html", {"profile": profile})

@login_required
def profile_edit(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        profile.bio = request.POST.get("bio")
        profile.website = request.POST.get("website")
        if request.FILES.get("avatar"):
            profile.avatar = request.FILES["avatar"]
        profile.save()
        return redirect("profile_view")
    return render(request, "profile/edit.html", {"profile": profile})

# === Posts ===
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/list.html", {"posts": posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        Comment.objects.create(
            post=post, author=request.user, content=request.POST["content"]
        )
        return redirect("post_detail", pk=pk)
    return render(request, "posts/detail.html", {"post": post})

@login_required
def post_create(request):
    if request.method == "POST":
        Post.objects.create(
            title=request.POST["title"],
            content=request.POST["content"],
            author=request.user,
        )
        return redirect("post_list")
    return render(request, "posts/create.html")

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect("post_list")
    if request.method == "POST":
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.save()
        return redirect("post_detail", pk=post.pk)
    return render(request, "posts/edit.html", {"post": post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
    return redirect("post_list")