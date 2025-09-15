from django.contrib import admin
from .models import UserProfile, Post, Comment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'website')
    list_filter = ('user__date_joined',)
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('user',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'comment_count')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Izohlar soni'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author').prefetch_related('comments')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content_preview', 'created_at')
    list_filter = ('created_at', 'post', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Izoh mazmuni'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post')

# Admin site customization
admin.site.site_header = "Blog Admin Paneli"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Blog boshqaruv paneli"
