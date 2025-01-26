document.addEventListener("DOMContentLoaded", () => {
    const updateCartItem = async (cartItemId, newQuantity, cartId) => {
      try {
        const response = await fetch("/cart/update_cart_item/", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
          },
          body: new URLSearchParams({
            cart_item_id: cartItemId,
            new_quantity: newQuantity,
            cart_id: cartId,
          }),
        });
  
        if (!response.ok) {
          throw new Error("Ошибка при обновлении корзины");
        }
  
        const data = await response.json();
        if (data.success) {
          // Обновляем отображение количества и цен
          const quantityInput = document.querySelector(`.quantity-input[data-cart-item-id="${data.cart_item_id}"]`);
          const itemPriceElement = document.querySelector(`.cart-item-total-price[data-cart-item-id="${data.cart_item_id}"]`);
          const cartTotalPriceElement = document.querySelector("#cart-total-price");
  
          quantityInput.value = data.cart_item_quantity;
          itemPriceElement.textContent = data.cart_item_total_price;
          cartTotalPriceElement.textContent = data.cart_total_price;
        } else {
          console.error("Ошибка при обновлении данных корзины");
        }
      } catch (error) {
        console.error("Ошибка:", error);
      }
    };
  
    document.querySelectorAll(".plus").forEach((button) => {
      button.addEventListener("click", () => {
        const cartItemId = button.dataset.cartItemId;
        const quantityInput = document.querySelector(`.quantity-input[data-cart-item-id="${cartItemId}"]`);
        const cartId = document.querySelector("#cart-total-price").dataset.cartId;
  
        let newQuantity = parseInt(quantityInput.value) + 1;
        updateCartItem(cartItemId, newQuantity, cartId);
      });
    });
  
    document.querySelectorAll(".minus").forEach((button) => {
      button.addEventListener("click", () => {
        const cartItemId = button.dataset.cartItemId;
        const quantityInput = document.querySelector(`.quantity-input[data-cart-item-id="${cartItemId}"]`);
        const cartId = document.querySelector("#cart-total-price").dataset.cartId;
  
        let newQuantity = Math.max(parseInt(quantityInput.value) - 1, 1); // Минимальное значение - 1
        updateCartItem(cartItemId, newQuantity, cartId);
      });
    });
  
    document.querySelectorAll(".quantity-input").forEach((input) => {
      input.addEventListener("change", () => {
        const cartItemId = input.dataset.cartItemId;
        const cartId = document.querySelector("#cart-total-price").dataset.cartId;
  
        let newQuantity = Math.max(parseInt(input.value), 1); // Минимальное значение - 1
        updateCartItem(cartItemId, newQuantity, cartId);
      });
    });
  });
  