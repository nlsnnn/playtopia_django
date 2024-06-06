$(document).ready(function () {
    let deleteUrl = $('.cart-list').data('delete-url');
    let addUrl = $('.cart-list').data('add-url');
    let subUrl = $('.cart-list').data('sub-url');
    let csrfToken = $('.cart-list').data('csrf-token');
    let amountText = document.getElementById('aText');

    $('.delete-from-cart').on('click', function () {
        let productId = $(this).data('product-id');
        $.ajax({
            url: deleteUrl,
            method: "POST",
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (response) {
                if (response.success) {
                    $('#product-' + productId).remove();
                    $('#p-'+productId).remove();
                    console.log(response.new_amount)
                    amountText.textContent = `${response.new_amount} руб.`;
                } else {
                    alert('Ошибка при удалении товара с корзины');
                }
            },
            error: function () {
                alert('Произошла ошибка.');
            }
        });
    });
    $('.add-item-cart').on('click', function () {
        let productId = $(this).data('product-id');
        let quantityText = document.getElementById('quantityText-'+productId);
        $.ajax({
            url: addUrl,
            method: "POST",
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (response) {
                if (response.success) {
                    console.log('Прибавили', 'quantityText-'+productId);
                    quantityText.textContent = response.quantity;
                    amountText.textContent = `${response.new_amount} руб.`;
                } else {
                    console.log('Ошибка при увеличении');
                }
            },
            error: function () {
                alert('Hmm....');
            }
        });
    });
    $('.sub-item-cart').on('click', function() {
        let productId = $(this).data('product-id');
        let quantityText = document.getElementById('quantityText-'+productId);

        $.ajax({
            url: subUrl,
            method: "POST",
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (response) {
                if (response.success) {
                    console.log(response.last)
                    if (response.last){
                        $('#product-' + productId).remove();
                        $('#p-' + productId).remove()
                        amountText.textContent = `${response.new_amount} руб.`;
                    } else{
                        console.log('Убавили');
                        quantityText.textContent=response.quantity;
                        amountText.textContent = `${response.new_amount} руб.`;
                    }
                } else {
                    console.log('Ошибка при уменьшении товара');
                }
            },
            error: function () {
                alert('Произошла ошибка');
            }
        });
    });
});
