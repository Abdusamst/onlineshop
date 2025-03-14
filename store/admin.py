from django.contrib import admin
from .models import Item, ItemTag, Poster, Seller, Review



@admin.register(Seller)  # Если @admin.register отсутствует, добавь его
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number', 'whatsapp', 'stock_status', 'store_address', 'seller_name']

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'slug', 'price',
                    'old_price', 'is_available', 'tag_list',)
    search_fields = ('title', 'description', 'tags__name',)
    list_filter = ('is_available', 'tags',)

    def short_description(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        else:   
            return obj.description

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    short_description.short_description = 'Описание'
    tag_list.short_description = 'Список категорий'


class ItemTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'short_description', 'item_list',)

    def short_description(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        else:
            return obj.description

    def item_list(self, obj):
        return [Item.objects.get(
            pk=o.get('object_id')
        ) for o in obj.items.values()]

    short_description.short_description = 'Описание'
    item_list.short_description = 'Список товаров'


# Создаем класс админки для Poster
class PosterAdmin(admin.ModelAdmin):
    list_display = ('image',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'rating', 'text', 'created_at')
    search_fields = ('user__username', 'item__title', 'text')
    list_filter = ('rating', 'created_at')
# Регистрация моделей с классами админки
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemTag, ItemTagAdmin)
admin.site.register(Poster, PosterAdmin)
admin.site.register(Review, ReviewAdmin)