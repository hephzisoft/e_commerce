$(document).ready(function () {

    let updateBtn = document.getElementsByClassName('update-cart')
    const update = document.querySelector('#update-form');
    const update_csrfToken = update.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const delete_form = document.querySelector('#delete-form');
    const delete_csrfToken = delete_form.querySelector('input[name="csrfmiddlewaretoken"]').value;





    for (let i = 0; i < updateBtn.length; i++) {
        updateBtn[i].addEventListener('click', function () {
            let action = this.dataset.action
            let btn = $(this)
            let id = $(this).attr('data-productId')
            let totalItemPrice = $('#item-total-price[data-productId=' + id + ']');
            let qty = $('#qty[data-productId=' + id + ']')
            

            $.ajax({
                url: '/update-cart/',
                type: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': update_csrfToken },
                data: JSON.stringify({
                    'id': id,
                    'action': action
                }),
                dataType: 'json',
                beforeSend: function () {
                    btn.attr('disabled', true)

                },
                success: function (response) {
                    if (response.qty <= 0 && action == 'remove') {
                        btn.attr('disabled', true)
                    }

                    qty.html(response.qty)
                    totalItemPrice.html("&#8358;" + response.item_total)

                    $(".cart-total-price").html("&#8358;" + response.orders_total)
                    btn.attr('disabled', false)
                }
            })
        })
    }

    $('.cart-item').each(function () {
        let id = $(this).find('#qty').attr('data-productId')
        let totalItemPrice = $('#item-total-price[data-productId=' + id + ']');
        let qty = $(this).find('#qty')
        $.ajax({
            url: '/cart-get-qty/' + id + '/',
            type: 'GET',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': update_csrfToken },
            dataType: 'json',
            success: function (response) {
                qty.html(response.qty)
                totalItemPrice.html("&#8358;" + response.item_total)
                $(".cart-total-price").html("&#8358;" + response.orders_total)

            }
        })
    });


    $('.delete-button').click(function (e) {
        e.preventDefault();
        let item_id = $(this).data('id');

        $.ajax({
            url: '/delete-item/' + item_id + '/',
            type: 'DELETE',
            headers: { 'X-CSRFToken': delete_csrfToken },
            success: function (response) {
                if (response.message === 'Item deleted successfully') {
                    $('#item-' + item_id).remove();
                    $(".cart-total-price").html("&#8358;" + response.orders_total)
                    if (response.orders_total >= 0) {
                        $(".cart-total-price").html("&#8358;" + response.orders_total)
                    } else {
                        $(".cart-total-price").html("&#8358;" + 0)
                    }
                } else {
                    alert('Failed to delete item');
                }
            }
        });
    });


})