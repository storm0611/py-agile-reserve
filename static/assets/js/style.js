// Show datatable 
new DataTable('#example', {
  paging: false,
  info: false,
  ordering: false,
});
// select datapicker
$(function () {
  $('#datepicker').datepicker();
});

// Book machine
$(".book_start").click(function () {
  var ipAddress = $(this).parent().parent().children(':nth-child(4)').text();
  var sn = $(this).parent().parent().children(':nth-child(3)').text();

  $('#ip_address').val(ipAddress);
  $('#sn').val(sn);
});

// End booked machine
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(".book_end").click(function () {
  var ipAddress = $(this).parent().parent().children(':nth-child(4)').text();
  var sn = $(this).parent().parent().children(':nth-child(3)').text();
  var data = JSON.stringify({ data: ipAddress, sn: sn })
  $.ajax({
    url: '/machine_end/',
    type: 'POST',
    dataType: "json",
    headers: {
      'X-CSRFToken': getCookie("csrftoken")
    },
    data: data,
    success: function (success) {
      console.log("response")
      location.reload();
    }
  });
})

// delete users
$(".selected_id").click(function() {
  var selected_user = $(this).parent().parent().children(':nth-child(2)').text();
  console.log("selected User", selected_user)
  $('#selected_user_id').val(selected_user);
})


