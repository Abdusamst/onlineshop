from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('about/', include('about.urls')),
    path('checkout/', include('checkout.urls')),
    path('users/', include('users.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('store.urls')),
    path('', include('django.contrib.auth.urls'))
]

urlpatterns += i18n_patterns(
    path('cart/', include('cart.urls')),
    path('store/', include('store.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
