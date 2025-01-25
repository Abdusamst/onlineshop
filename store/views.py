from django.shortcuts import render
from .models import Item, ItemTag, Poster, Favorite
from .paginator import paginator

def store(request):
    items = Item.objects.filter(is_available=True)
    tags = ItemTag.objects.all().order_by('name')  # Добавим сортировку
    posters = Poster.objects.all()
    favorites = Favorite.objects.filter(user=request.user).values_list('item_id', flat=True) if request.user.is_authenticated else []
    context = {
        'page_obj': paginator(request, items, 9),
        'page_obj_2': tags,  # Обновим контекст для тегов
        'range': [*range(1, 7)],  # For random css styles
        'posters': posters,
        'favorites': favorites,
    }
    return render(request, 'store/main_page.html', context)




def poster(request):
    posters = Poster.objects.all()
    context = {
        'posters': posters,
    }
    return render(request, 'store/poster.html', context)

def item_details(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, item=item).exists()
    context = {
        'item': item,
        'is_favorite': is_favorite,
    }
    return render(request, 'store/item_details.html', context)

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import ItemTag, Item

def tag_details(request, slug):
    tag = get_object_or_404(ItemTag, slug=slug)
    items = Item.objects.filter(tags=tag)  # Вместо tags__in=[tag]
    paginator = Paginator(items, 10)  # отобразить 10 товаров на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'page_obj': page_obj,
    }

    return render(request, 'store/tag_details.html', context)


def tag_list(request):
    tags = ItemTag.objects.all()
    context = {
        'page_obj': paginator(request, tags, 6),
    }
    return render(request, 'store/tag_list.html', context)



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Favorite, Item

@login_required
def add_to_favorites(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    Favorite.objects.get_or_create(user=request.user, item=item)
    return redirect(reverse('store:item_details', kwargs={'item_slug': item.slug}))

@login_required
def remove_from_favorites(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    favorite = get_object_or_404(Favorite, user=request.user, item=item)
    favorite.delete()
    return redirect(reverse('store:item_details', kwargs={'item_slug': item.slug}))

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {
        'favorites': favorites,
    }
    return render(request, 'store/favorite_list.html', context)




from django.http import JsonResponse

@login_required
def toggle_favorite(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)
    if not created:
        favorite.delete()
        action = 'removed'
    else:
        action = 'added'
    return JsonResponse({'action': action})

from django.db.models import Q
from django.shortcuts import render
from .models import Item, ItemTag

def search(request):
    query = request.GET.get('q')
    if query:
        results = Item.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        results = Item.objects.all()  # Показываем все товары, если запрос пуст
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'store/search.html', context)


from .forms import SellerRegistrationForm

from django.shortcuts import render, redirect
from .forms import SellerRegistrationForm, ItemForm
from .models import Seller, Item

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SellerRegistrationForm
from .models import User, Seller

@login_required
def become_seller(request):
    if request.user.is_seller:
        messages.info(request, 'Вы уже продавец.')
        return redirect('store:home')

    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()
            request.user.is_seller = True
            request.user.save()
            return redirect('store:add_item')  # Перенаправление на добавление товара
    else:
        form = SellerRegistrationForm()
        
    return render(request, 'store/becomeseller.html', {'form': form})




@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user  # Используйте объект CustomUser вместо Seller
            item.save()
            return redirect('store:my_items')
    else:
        form = ItemForm()
    return render(request, 'store/add_item.html', {'form': form})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item

@login_required
def my_items(request):
    seller = request.user
    items = Item.objects.filter(seller=seller)
    return render(request, 'store/my_items.html', {'items': items})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, seller=request.user)  # Используйте объект CustomUser вместо Seller
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('store:my_items')
    else:
        form = ItemForm(instance=item)
    return render(request, 'store/edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, seller=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('store:my_items')
    return render(request, 'store/delete_item.html', {'item': item})
