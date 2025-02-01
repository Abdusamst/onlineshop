from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager 
from taggit .models import GenericTaggedItemBase, TagBase
from django.utils.text import slugify
from django.conf import settings


class ItemTag(TagBase):
    image = models.ImageField(
        upload_to='categories/',
        verbose_name='Изображение',
        blank=True
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    item = models.ForeignKey(
        'store.Item',
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )

class TaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ItemTag,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name='Категория',
    )


class Poster(models.Model):
    image = models.ImageField(
        upload_to='posters/',
        verbose_name='Изображение',
        blank=True
    )

    class Meta:
        verbose_name = _("Постер")
        verbose_name_plural = _("Постеры")

    def __str__(self):
        return f"Poster {self.id}"



class Item(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название',)
    description = models.TextField(verbose_name='Описание',)
    slug = models.SlugField(
        unique=True,
        blank=True,
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления',)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Новая цена',
    )
    old_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Старая цена',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='items/',
        blank=True,
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступно',
    )
    tags = TaggableManager(through=TaggedItem, related_name="tagged_items", verbose_name='Категории',)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default = 1 ,related_name='items', verbose_name='Продавец')
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:  # если slug еще не создан
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Item.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-price']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller', verbose_name='Пользователь')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    whatsapp = models.CharField(max_length=20, verbose_name='WhatsApp')
    STORE_TYPE_CHOICES = [
        ('warehouse', 'Склад'),
        ('shop', 'Магазин'),
        ('online_shop', 'Интернет-магазин'),
    ]
    store_type = models.CharField(max_length=20, choices=STORE_TYPE_CHOICES, verbose_name='Тип магазина')
    STOCK_STATUS_CHOICES = [
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'Нет в наличии'),
        ('partial_stock', 'Частично в наличии'),
    ]
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, verbose_name='Статус наличия товара')
    store_address = models.CharField(max_length=255, verbose_name='Адрес магазина или склада')
    store_name = models.CharField(max_length=255, verbose_name='Название магазина')
    store_logo = models.ImageField(upload_to='store_logos/', verbose_name='Логотип магазина')
    seller_name = models.CharField(max_length=255, verbose_name='Имя и фамилия продавца')
    wants_to_sell_on_wildberries = models.BooleanField(default=False, verbose_name='Хотите продавать на Wildberries')
    wants_to_sell_on_ozon = models.BooleanField(default=False, verbose_name='Хотите продавать на Ozon')
    has_store_on_wildberries = models.BooleanField(default=False, verbose_name='Есть магазин на Wildberries')
    has_store_on_ozon = models.BooleanField(default=False, verbose_name='Есть магазин на Ozon')

    def __str__(self):
        return self.store_name

