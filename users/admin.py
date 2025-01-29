from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_name', 'feedback_email',
                    'feedback_message', 'created_at',)
    ordering = ('-created_at',)


admin.site.register(Feedback, FeedbackAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Регистрируем модель CustomUser в админке, используя UserAdmin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'is_superuser', 'is_staff', 'is_seller', 'is_phone_verified']
    list_filter = ['is_superuser', 'is_staff', 'is_seller']
    search_fields = ['username', 'email', 'phone_number']
    ordering = ['username']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'is_phone_verified', 'is_seller')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'is_phone_verified', 'is_seller')}),
    )

# Регистрируем модель CustomUser с CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
