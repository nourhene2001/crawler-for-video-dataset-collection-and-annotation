$(document).ready(function() {
     
    $('.existing').hide(); 
    $('button').click(function() {
        // hide the button that was clicked
        if ($(this).attr('id') == 'existing') {
            $('.existing').show();
            $('.option').hide(); // hide the button that was clicked
        }
    });
});
