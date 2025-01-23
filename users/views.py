import asyncio

import telegram
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from OnlineStore.settings import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
from checkout.models import Order
from .forms import CreationForm, FeedbackForm
from .models import Feedback


@login_required
def user_orders(request):
    """
    Представление списка заказов пользователя.
    """
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'users/user_orders.html', context)


@login_required
def profile(request):
    """
    Представление профиля пользователя.
    """
    return render(request, 'users/profile.html')


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser
from .utils import send_email_notification  # удалил send_sms_notification

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('store:home')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        email = form.cleaned_data.get('email')
        phone_number = form.cleaned_data.get('phone_number')
        if email:
            send_email_notification(email)
        elif phone_number:
            # Здесь можно добавить логику для отправки SMS через выбранный вами сервис
            pass
        return response



async def send_telegram_message(message):
    """
    Асинхронная функция для отправки сообщения в ТГ.
    """
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    chat_id = TELEGRAM_CHAT_ID
    await bot.send_message(chat_id=chat_id, text=message)


def feedback_processing(request):
    """
    Представление приема и обработки для обратной связи.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(
                feedback_name=form.cleaned_data['feedback_name'],
                feedback_email=form.cleaned_data['feedback_email'],
                feedback_message=form.cleaned_data['feedback_message'],
            )
            feedback.save()

            # Отпрака сообщения
            message = f"Новое сообщение от {feedback.feedback_name} ({feedback.feedback_email}): {feedback.feedback_message}"
            asyncio.run(send_telegram_message(message))

            return render(request, 'users/feedback_success.html')
    return render(request, 'users/feedback_failed.html')

