function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

function editField(event, itemId, fieldName, fieldValue) {
  // Get the cell that was clicked
  const cell = event.target;

  // Create a new input field
  const inputField = document.createElement('input');
  inputField.type = 'text';
  inputField.value = fieldValue;

  // Replace the text in the cell with the input field
  cell.textContent = '';
  cell.appendChild(inputField);

  // Set focus on the input field
  inputField.focus();

  // Add an event listener to the input field
  inputField.addEventListener('blur', function() {
    const newValue = inputField.value;

    // Send the new value to the server using an AJAX request
    const xhr = new XMLHttpRequest();
    const url = '/update_d/';
    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
      if (xhr.status === 200) {
        // Replace the input field with the new value
        cell.removeChild(inputField);
        cell.textContent = newValue;
      }
    };
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    const csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xhr.send(`item_id=${itemId}&field_name=${fieldName}&field_value=${newValue}&csrfmiddlewaretoken=${csrfmiddlewaretoken}`);
  });
}
