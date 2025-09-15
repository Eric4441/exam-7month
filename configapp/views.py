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
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db import models

# Home page - Welcome page
def index(request):
    # Get some statistics for the homepage
    total_posts = Post.objects.count()
    total_users = User.objects.count()
    total_comments = Comment.objects.count()
    
    # Get recent posts for featured section
    recent_posts = Post.objects.order_by('-created_at')[:3]
    
    # Get top contributors (users with most posts)
    top_contributors = User.objects.annotate(
        post_count=models.Count('posts')
    ).filter(post_count__gt=0).order_by('-post_count')[:5]
    
    context = {
        'total_posts': total_posts,
        'total_users': total_users,
        'total_comments': total_comments,
        'recent_posts': recent_posts,
        'top_contributors': top_contributors,
    }
    return render(request, 'home/index.html', context)

# Admin check decorator
def admin_required(user):
    return user.is_staff or user.is_superuser

# Frontend Admin Views
@user_passes_test(admin_required)
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_posts = Post.objects.order_by('-created_at')[:5]
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'active_users': active_users,
        'recent_users': recent_users,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
    }
    return render(request, 'admin_frontend/dashboard.html', context)

@user_passes_test(admin_required)
def admin_users(request):
    """Manage users"""
    users_list = User.objects.all().order_by('-date_joined')
    
    # Search functionality
    search = request.GET.get('search', '')
    if search:
        users_list = users_list.filter(
            username__icontains=search
        ) | users_list.filter(
            email__icontains=search
        ) | users_list.filter(
            first_name__icontains=search
        ) | users_list.filter(
            last_name__icontains=search
        )
    
    # Pagination
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'admin_frontend/users.html', {
        'users': users,
        'search': search
    })

@user_passes_test(admin_required)
def admin_user_detail(request, user_id):
    """User detail and edit"""
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Update user info
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.is_active = 'is_active' in request.POST
        user.is_staff = 'is_staff' in request.POST
        user.save()
        
        # Update profile
        profile.bio = request.POST.get('bio', '')
        profile.website = request.POST.get('website', '')
        profile.save()
        
        messages.success(request, f'{user.username} ma\'lumotlari yangilandi!')
        return redirect('admin_user_detail', user_id=user.id)
    
    user_posts = user.posts.all()[:5]
    user_comments = user.comment_set.all()[:5]
    
    return render(request, 'admin_frontend/user_detail.html', {
        'user_obj': user,
        'profile': profile,
        'user_posts': user_posts,
        'user_comments': user_comments,
    })

@user_passes_test(admin_required)
def admin_posts(request):
    """Manage posts"""
    posts_list = Post.objects.all().order_by('-created_at')
    
    # Search functionality
    search = request.GET.get('search', '')
    if search:
        posts_list = posts_list.filter(
            title__icontains=search
        ) | posts_list.filter(
            content__icontains=search
        ) | posts_list.filter(
            author__username__icontains=search
        )
    
    # Filter by author
    author_filter = request.GET.get('author', '')
    if author_filter:
        posts_list = posts_list.filter(author__username__icontains=author_filter)
    
    # Pagination
    paginator = Paginator(posts_list, 15)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'admin_frontend/posts.html', {
        'posts': posts,
        'search': search,
        'author_filter': author_filter
    })

@user_passes_test(admin_required)
def admin_comments(request):
    """Manage comments"""
    comments_list = Comment.objects.all().order_by('-created_at')
    
    # Search functionality
    search = request.GET.get('search', '')
    if search:
        comments_list = comments_list.filter(
            content__icontains=search
        ) | comments_list.filter(
            author__username__icontains=search
        ) | comments_list.filter(
            post__title__icontains=search
        )
    
    # Filter by post
    post_filter = request.GET.get('post', '')
    if post_filter:
        comments_list = comments_list.filter(post__title__icontains=post_filter)
    
    # Pagination
    paginator = Paginator(comments_list, 20)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    
    return render(request, 'admin_frontend/comments.html', {
        'comments': comments,
        'search': search,
        'post_filter': post_filter
    })

@user_passes_test(admin_required)
def admin_delete_comment(request, comment_id):
    """Delete comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Izoh o\'chirildi!')
    return redirect('admin_comments')

@user_passes_test(admin_required)
def admin_delete_post(request, post_id):
    """Delete post"""
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post o\'chirildi!')
    return redirect('admin_posts')
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
    """Create demo data for the blog"""
    # Check if demo data already exists
    if User.objects.filter(username="demo").exists():
        return Response({"message": "Demo ma'lumotlar allaqachon mavjud!"})
    
    # Create demo user
    demo_user = User.objects.create_user(
        username="demo",
        password="demo123",
        email="demo@example.com",
        first_name="Demo",
        last_name="User"
    )
    
    # Create user profile
    UserProfile.objects.create(
        user=demo_user,
        bio="Men demo foydalanuvchiman. Bu blog platformasini sinab ko'rish uchun yaratilganman.",
        website="https://example.com"
    )
    
    # Create demo posts
    posts_data = [
        {
            "title": "Blog platformasiga xush kelibsiz!",
            "content": """Bu bizning yangi blog platformasi. Bu yerda siz:

• O'z postlaringizni yozishingiz
• Boshqa foydalanuvchilar postlariga izoh qoldirshingiz
• O'z profilingizni sozlashingiz
• Boshqa bloggerlar bilan muloqot qilishingiz mumkin

Omad tilaymiz!"""
        },
        {
            "title": "Django bilan blog yaratish",
            "content": """Django - bu Python tilida yozilgan kuchli web framework. U yordamida:

1. Tez va oson web ilovalar yaratish mumkin
2. Admin paneli avtomatik yaratiladi
3. Xavfsizlik yuqori darajada ta'minlanadi
4. Ko'plab tayyor komponentlar mavjud

Bu blog ham Django yordamida yaratilgan!"""
        },
        {
            "title": "Birinchi postingizni qanday yozish kerak",
            "content": """Yaxshi post yozish uchun quyidagi maslahatlarni bajaring:

📝 **Aniq sarlavha qo'ying**
Sarlavha postingizning mohiyatini aks ettirishi kerak.

📖 **Tushunarli yozing**
Oddiy va tushunarli til ishlating.

🎯 **Maqsadni belgilang**
Nima haqida yozayotganingizni aniq belgilang.

💡 **Foydali ma'lumot bering**
O'quvchilar uchun qiziq va foydali kontent yarating.

Omad tilaymiz!"""
        }
    ]
    
    created_posts = []
    for post_data in posts_data:
        post = Post.objects.create(
            author=demo_user,
            title=post_data["title"],
            content=post_data["content"]
        )
        created_posts.append(post)
    
    # Create demo comments
    comments_data = [
        "Ajoyib post! Rahmat ma'lumot uchun.",
        "Juda foydali bo'ldi, davom eting!",
        "Qiziq yozuv, boshqa postlarni ham kutaman.",
        "Bu ma'lumot menga juda kerak edi, rahmat!",
        "Zo'r tushuntirgan, tushunarli yozilgan."
    ]
    
    for i, post in enumerate(created_posts):
        # Add some comments to each post
        for j in range(min(3, len(comments_data))):
            Comment.objects.create(
                post=post,
                author=demo_user,
                content=comments_data[(i + j) % len(comments_data)]
            )
    
    return Response({
        "message": "Demo ma'lumotlar muvaffaqiyatli yaratildi!",
        "details": {
            "user": "demo",
            "password": "demo123",
            "posts": len(created_posts),
            "comments": Comment.objects.filter(author=demo_user).count()
        }
    })
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/list.html", {"posts": posts})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile for the new user
            UserProfile.objects.create(user=user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
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
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "profile/view.html", {"profile": profile})

@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.bio = request.POST.get("bio", "")
        profile.website = request.POST.get("website", "")
        if request.FILES.get("avatar"):
            profile.avatar = request.FILES["avatar"]
        profile.save()
        messages.success(request, "Profil muvaffaqiyatli yangilandi!")
        return redirect("profile_view")
    return render(request, "profile/edit.html", {"profile": profile})

# === Posts ===
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/list.html", {"posts": posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get("content", "").strip()
        if content:
            Comment.objects.create(
                post=post, author=request.user, content=content
            )
            messages.success(request, "Izoh muvaffaqiyatli qo'shildi!")
        return redirect("post_detail", pk=pk)
    return render(request, "posts/detail.html", {"post": post})

@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        if title and content:
            Post.objects.create(
                title=title,
                content=content,
                author=request.user,
            )
            messages.success(request, "Post muvaffaqiyatli yaratildi!")
            return redirect("post_list")
        else:
            messages.error(request, "Barcha maydonlarni to'ldiring!")
    return render(request, "posts/create.html")

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "Siz faqat o'zingizning postingizni tahrirlashingiz mumkin!")
        return redirect("post_list")
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, "Post muvaffaqiyatli yangilandi!")
            return redirect("post_detail", pk=post.pk)
        else:
            messages.error(request, "Barcha maydonlarni to'ldiring!")
    return render(request, "posts/edit.html", {"post": post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, "Post muvaffaqiyatli o'chirildi!")
    else:
        messages.error(request, "Siz faqat o'zingizning postingizni o'chirishingiz mumkin!")
    return redirect("post_list")