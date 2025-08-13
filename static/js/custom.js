document.addEventListener('DOMContentLoaded', function() {
  const decreaseBtn = document.querySelector('.btn-decrease');
  const increaseBtn = document.querySelector('.btn-increase');
  const quantityInput = document.getElementById('quantity-input');

  decreaseBtn.addEventListener('click', function() {
    let current = parseInt(quantityInput.value, 10);
    if (current > 1) {
      quantityInput.value = current - 1;
    }
  });

  increaseBtn.addEventListener('click', function() {
    let current = parseInt(quantityInput.value, 10);
    quantityInput.value = current + 1;
  });
});

