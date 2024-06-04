$(document).ready(function () {
    let deleteUrl = $('.cart-list').data('delete-url');
    let addUrl = $('.cart-list').data('add-url');
    let subUrl = $('.cart-list').data('sub-url');
    let csrfToken = $('.cart-list').data('csrf-token');

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
                    alert('Товар убран!');
                    $('#product-' + productId).remove();
                    $('#p-'+productId).remove();
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
                    quantityText.textContent=response.quantity;
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
                        console.log('#p-' + productId)
                    } else{
                        console.log('Убавили');
                        quantityText.textContent=response.quantity;
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
