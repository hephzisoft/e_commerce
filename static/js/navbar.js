$(document).ready(function () {
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    var cart = $('.cart-count')
    $.ajax({
      url: '/update-cart/',
        type: 'GET',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf_token },
        success:function (response){
            cart.html(response.counts)
        }

    })
  })