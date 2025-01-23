from urllib.parse import urlencode

def generate_whatsapp_message(cart_items):
    base_url = "https://wa.me/+998997966517"
    message = "Здравствуйте! Я хочу оформить заказ. Вот список товаров:\n\n"

    total_cost = 0
    for item in cart_items:
        item_total = item.quantity * item.item.price
        message += f"- {item.item.title}: {item.quantity} шт. x {item.item.price} сум = {item_total} сум\n"
        total_cost += item_total

    message += f"\nОбщая стоимость: {total_cost} kg"
    params = urlencode({'text': message})
    return f"{base_url}?{params}"
