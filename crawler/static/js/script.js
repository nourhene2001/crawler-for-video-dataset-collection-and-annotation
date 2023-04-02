$(document).ready(function() {
  
    
const form3 = document.querySelector('#form3');
const form2 = document.querySelector('#form2');
const submitButton = form3.querySelector('button[class="cta"]');

submitButton.addEventListener('click', () => {
  const name = form3.querySelector('#id_form3_name').value;
  form2.action = `{% url "update" name="${name}" %}`;
});

});