from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

class Feedback(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="feedbacks", null=True, blank=True, verbose_name="Пользователь")
    feedback_name = models.CharField(max_length=50, verbose_name="Имя покупателя")
    feedback_email = models.EmailField(verbose_name="Почта покупателя")
    feedback_message = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Обратная связь покупателя"
        verbose_name_plural = "Обратная связь покупателей"

    def __str__(self):
        return self.feedback_message[:30]


# Менеджер пользователей
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Имя пользователя обязательно!")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False, verbose_name="Продавец")
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True, verbose_name="Номер телефона")
    is_phone_verified = models.BooleanField(default=False, verbose_name="Телефон подтвержден")
    avatar = models.ImageField(upload_to="avatars/", default="images/user.png", verbose_name="Аватар")

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_set_permissions", blank=True)

    objects = CustomUserManager()


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
