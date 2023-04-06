$(document).ready(function () {
  const qty = $('#qty')
  const csrf_token = $('input[name=csrfmiddlewaretoken]').val()
  const id = document.getElementById('product-id').value
  const updateBtn = document.getElementsByClassName('update-cart')
  $.ajax({
    url: '/get-qty/' + id + '/',
    type: 'GET',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf_token },
    dataType: 'json',
    success: function (response) {
      qty.html(response.qty)
    }
  })
  for (let i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
      const action = this.dataset.action
      const btn = $(this)
      console.log(action)
      console.log(id)
     

      $.ajax({
        url: '/update-cart/',
        type: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf_token },
        data: JSON.stringify({
          'action': action,
          'id': id
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
          btn.attr('disabled', false)
        }
      })
    })
  }
})