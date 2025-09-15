from django.db import models
from django.contrib.auth.models import User,BaseUserManager, AbstractBaseUser, PermissionsMixin
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


# class CustomUserManager(BaseUserManager):
#     def create_user(self, phone, password=None, **extra_fields):
#         if not phone:
#             raise ValueError("Telefon raqam kiritilishi shart")
#         user = self.model(phone=phone, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, phone, password=None, **extra_fields):
#         extra_fields.setdefault("is_admin", True)
#         extra_fields.setdefault("is_staff", True)
#
#         if extra_fields.get("is_admin") is not True:
#             raise ValueError("Superuser is_admin=True bo‘lishi kerak!")
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser is_staff=True bo‘lishi kerak!")
#
#         return self.create_user(phone, password, **extra_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     phone = models.CharField(max_length=15, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = "phone"
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.phone