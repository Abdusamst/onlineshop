import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnlineStore.settings")  # Замените "onlineshop" на ваш проект!
django.setup()

from users.models import CustomUser

superuser, created = CustomUser.objects.get_or_create(
    username="admin",
    defaults={
        "phone_number": "+998997966517",
        "is_superuser": True,
        "is_staff": True
    }
)
if created:
    superuser.set_password("adminpassword")
    superuser.save()
    print("Суперпользователь создан!")
else:
    print("Суперпользователь уже существует!")
