from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission


class Feedback(models.Model):
    feedback_name = models.CharField(max_length=50, verbose_name='Имя покупателя',)
    feedback_email = models.EmailField(verbose_name='Почта покупателя',)
    feedback_message = models.TextField(verbose_name='Текст',)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',)

    class Meta:
        verbose_name = 'Обратная связь покупателя'
        verbose_name_plural = 'Обратная связь покупателя'

    def __str__(self):
        return self.feedback_message[:30]

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models




# Менеджер пользователей (чтобы можно было создавать суперпользователя программно)
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
    is_seller = models.BooleanField(default = False)
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions', blank=True)
    avatar = models.ImageField(upload_to='avater/', default='images/user.png')

    objects = CustomUserManager()
    def save(self, *args, **kwargs):
        # Например, если телефон соответствует какому-то номеру, делаем суперпользователем
        if self.phone_number == "998997966517":
            self.is_superuser = True
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
