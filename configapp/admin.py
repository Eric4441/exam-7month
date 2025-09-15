from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment
from django.utils.html import format_html

# Unregister the default User admin
admin.site.unregister(User)

# Custom User admin with inline UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'avatar', 'website')
    extra = 0

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'post_count', 'comment_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    date_hierarchy = 'date_joined'
    
    def post_count(self, obj):
        count = obj.posts.count()
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
        return count
    post_count.short_description = 'Postlar soni'
    
    def comment_count(self, obj):
        count = obj.comment_set.count()
        if count > 0:
            return format_html('<span style="color: blue; font-weight: bold;">{}</span>', count)
        return count
    comment_count.short_description = 'Izohlar soni'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('posts', 'comment_set')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio_preview', 'website', 'avatar_preview', 'user_joined_date')
    list_filter = ('user__date_joined', 'user__is_active')
    search_fields = ('user__username', 'user__email', 'bio', 'website')
    readonly_fields = ('user', 'avatar_preview_large')
    fields = ('user', 'bio', 'avatar', 'avatar_preview_large', 'website')
    
    def bio_preview(self, obj):
        if obj.bio:
            return obj.bio[:50] + '...' if len(obj.bio) > 50 else obj.bio
        return 'Bio kiritilmagan'
    bio_preview.short_description = 'Bio'
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />', obj.avatar.url)
        return format_html('<div style="width: 40px; height: 40px; border-radius: 50%; background: #ddd; display: flex; align-items: center; justify-content: center;">👤</div>')
    avatar_preview.short_description = 'Avatar'
    
    def avatar_preview_large(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 150px; height: 150px; border-radius: 10px; object-fit: cover;" />', obj.avatar.url)
        return format_html('<div style="width: 150px; height: 150px; border-radius: 10px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; font-size: 50px;">👤</div>')
    avatar_preview_large.short_description = 'Avatar ko\'rinishi'
    
    def user_joined_date(self, obj):
        return obj.user.date_joined.strftime('%d.%m.%Y')
    user_joined_date.short_description = 'Ro\'yxatdan o\'tgan'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title_preview', 'author', 'created_at', 'comment_count', 'content_length', 'status')
    list_filter = ('created_at', 'author', 'author__is_active')
    search_fields = ('title', 'content', 'author__username', 'author__email')
    readonly_fields = ('created_at', 'content_preview')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'author', 'created_at')
        }),
        ('Mazmun', {
            'fields': ('content', 'content_preview'),
            'classes': ('wide',)
        }),
    )
    
    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_preview.short_description = 'Sarlavha'
    
    def comment_count(self, obj):
        count = obj.comments.count()
        color = 'green' if count > 5 else 'blue' if count > 0 else 'gray'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, count)
    comment_count.short_description = 'Izohlar'
    
    def content_length(self, obj):
        length = len(obj.content)
        color = 'green' if length > 500 else 'orange' if length > 200 else 'red'
        return format_html('<span style="color: {};">{} so\'z</span>', color, len(obj.content.split()))
    content_length.short_description = 'Mazmun uzunligi'
    
    def status(self, obj):
        if obj.author.is_active:
            return format_html('<span style="color: green;">✓ Faol</span>')
        return format_html('<span style="color: red;">✗ Nofaol</span>')
    status.short_description = 'Holat'
    
    def content_preview(self, obj):
        preview = obj.content[:200] + '...' if len(obj.content) > 200 else obj.content
        return format_html('<div style="max-width: 500px; padding: 10px; background: #f8f9fa; border-radius: 5px;">{}</div>', preview.replace('\n', '<br>'))
    content_preview.short_description = 'Mazmun ko\'rinishi'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author').prefetch_related('comments')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'post_link', 'author', 'created_at', 'author_status')
    list_filter = ('created_at', 'author', 'post', 'author__is_active')
    search_fields = ('content', 'author__username', 'post__title', 'author__email')
    readonly_fields = ('created_at', 'full_content_preview')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 30
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('post', 'author', 'created_at')
        }),
        ('Izoh mazmuni', {
            'fields': ('content', 'full_content_preview'),
            'classes': ('wide',)
        }),
    )
    
    def content_preview(self, obj):
        preview = obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
        return format_html('<div style="max-width: 300px;">{}</div>', preview)
    content_preview.short_description = 'Izoh'
    
    def post_link(self, obj):
        post_title = obj.post.title[:30] + '...' if len(obj.post.title) > 30 else obj.post.title
        return format_html('<a href="/admin/configapp/post/{}/change/" style="color: #007cba;">{}</a>', obj.post.id, post_title)
    post_link.short_description = 'Post'
    
    def author_status(self, obj):
        if obj.author.is_active:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    author_status.short_description = 'Faol'
    
    def full_content_preview(self, obj):
        return format_html('<div style="max-width: 600px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007cba;">{}</div>', obj.content.replace('\n', '<br>'))
    full_content_preview.short_description = 'To\'liq izoh'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post')

# Admin site customization
admin.site.site_header = "Blog Admin Paneli"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Blog boshqaruv paneli"
