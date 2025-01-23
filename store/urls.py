from django.urls import path
from .views import item_details, store, tag_details, tag_list, add_to_favorites, remove_from_favorites, favorite_list, toggle_favorite, search, become_seller, add_item

app_name = 'store'

urlpatterns = [
    path('', store, name='home'),
    path('categories/', tag_list, name='tag_list'),
    path('category-details/<slug:slug>/', tag_details, name='tag_details'),
    path('search/', search, name='search'),  # Маршрут для поиска
    path('favorites/', favorite_list, name='favorite_list'),  # Маршрут для списка избранного
    path('add_to_favorites/<int:item_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:item_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('toggle_favorite/<int:item_id>/', toggle_favorite, name='toggle_favorite'),
    path('become-seller/', become_seller, name='becomeseller'),  # Маршрут для регистрации продавца
    path('add-item/', add_item, name='add_item'),
    path('<slug:item_slug>/', item_details, name='item_details'),  # Маршрут для деталей товара
]
