from django.core.mail import send_mail

def send_email_notification(email):
    send_mail(
        'Регистрация успешна',
        'Спасибо за регистрацию!',
        'noreply@example.com',
        [email],
        fail_silently=False,
    )

def send_sms_notification(phone_number):
    from twilio.rest import Client

    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='Спасибо за регистрацию!',
        to=phone_number
    )
