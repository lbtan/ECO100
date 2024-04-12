/* Based on some code from ChatGPT */
$(document).ready(function(){

    function show_appt() {
        console.log("Button clicked.");
        var params = {
            tutor_netid: $(this).data('tutor_netid'),
            date: $(this).data('date'),
            time: $(this).data('time')
        };
        var urlParams = $.param(params);
        console.log(params) 

        // Load the popup HTML using AJAX
        $.get('/appointment_popup?' + urlParams, function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
                        
            // Add the modified HTML to the modal container and show the modal
            $('#modal-container').html($modal);
            $('#appointmentModal').modal('show');
        });
    }

    // Event binding for button click
    $('.time-slot').click(show_appt);
    $('.view-cancel').click(show_appt)
});
