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
    inputField.classList.add('input-field'); // Add a class to the input field
   
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
      const url = '/update_dataset/';
      xhr.open('POST', url);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
      xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

      xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('hh')
          // Replace the input field with the new value
          cell.removeChild(inputField);
          cell.textContent = newValue;
        }
      };
      const data = {
        data_id: itemId,
        field_name: fieldName,
        field_value: newValue,
      };
      console.log(data)
      xhr.send(JSON.stringify(data));
    });
  }
  function deleteItem(itemId) {
    
    // Send the new value to the server using an AJAX request
    const xhr = new XMLHttpRequest();
    const url = '/delete/';
    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    xhr.onload = function() {
      if (xhr.status === 200) {
          console.log('hh')
        // Replace the input field with the new value
        
      }
    };
  }
  
  
  