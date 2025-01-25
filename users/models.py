from django.db import models
from django.contrib.auth.models import AbstractUser

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

class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default = False)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions', blank=True)

    def __str__(self):
        return self.username
