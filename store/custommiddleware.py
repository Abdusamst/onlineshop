from django.utils import translation

class CustomLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Определение языка (порядок проверки можно изменить)
        lang = (
            request.GET.get('lang') or                  # Параметр в URL (например, ?lang=ru)
            request.COOKIES.get('django_language') or   # Куки
            request.session.get('django_language') or   # Сессия
            'en'                                        # Язык по умолчанию
        )

        # 2. Установите текущий язык
        translation.activate(lang)
        request.LANGUAGE_CODE = lang

        # 3. Ответ
        response = self.get_response(request)

        # 4. Установите язык в куки (опционально)
        response.set_cookie('django_language', lang)

        return response
