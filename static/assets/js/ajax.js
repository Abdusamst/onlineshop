document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.minus, .plus').forEach(function(button) {
      button.addEventListener('click', function() {
        var cartItemId = this.getAttribute('data-cart-item-id');
        var input = document.querySelector('.quantity-input[data-cart-item-id="' + cartItemId + '"]');
        var count = parseInt(input.value);
  
        if (this.classList.contains('minus')) {
          count = count > 1 ? count - 1 : 1;
        } else {
          count = count + 1;
        }
  
        input.value = count;
        updateCartItem(cartItemId, count);
      });
    });
  
    function updateCartItem(cartItemId, newQuantity) {
      var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      var cartId = document.querySelector('#cart-total-price').getAttribute('data-cart-id');
  
      fetch('/update_cart_item/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          cart_id: cartId,
          new_quantity: newQuantity,
          cart_item_id: cartItemId,
        }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          var newTotalPrice = data.cart_item_total_price;
          var newCartTotalPrice = data.cart_total_price;
  
          document.querySelector('.quantity-input[data-cart-item-id="' + cartItemId + '"]').value = data.cart_item_quantity;
          document.querySelector('.cart-item-total-price[data-cart-item-id="' + cartItemId + '"]').innerText = newTotalPrice;
          document.querySelector('#cart-total-price').innerText = newCartTotalPrice;
  
          console.log('Successfully updated');
        } else {
          console.error('Failed to update cart item:', data.error);
        }
      })
      .catch(error => console.error('Error:', error));
    }
  });
  