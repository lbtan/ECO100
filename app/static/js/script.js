$(document).ready(function(){

    function show_appt() {
        var params = {
            tutor_netid: $(this).data('tutor_netid'),
            date: $(this).data('date'),
            time: $(this).data('time')
        };
        var urlParams = $.param(params);
        
        // Modal (popup) code from ChatGPT
        // Load the popup HTML using AJAX
        $.get('/appointment_popup?' + urlParams, function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
                        
            // Add the modified HTML to the modal container and show the modal
            $('#modal-container').html($modal);
            $('#appointmentModal').modal('show');
        });
    }

    function add_appt_time() {
        var params = {
            tutor_netid: $(this).data('tutor_netid'),
            date: $(this).data('date'),
        };
        var urlParams = $.param(params);
        
        // Modal (popup) code from ChatGPT
        // Load the popup HTML using AJAX
        $.get('/add_appointment?' + urlParams, function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
                        
            // Add the modified HTML to the modal container and show the modal
            $('#add-appt-modal-container').html($modal);
            $('#addAppointmentModal').modal('show');
        });
    }

    function show_tutor_overview() {
        // Load the popup HTML using AJAX
        $.get('/tutor_overview', function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
            // Add the modified HTML to the modal container and show the modal
            $('#overview-modal-container').html($modal);
            $('#overviewModal').modal('show');
        });
    }

    function show_weekly_summary() {
        // Load the popup HTML using AJAX
        $.get('/weekly_summary', function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
            // Add the modified HTML to the modal container and show the modal
            $('#summary-modal-container').html($modal);
            $('#summaryModal').modal('show');
        });
    }

    function show_tutor_bio_edit() {

        var params = {
            tutor_netid: $(this).data('tutor_netid'),
            bio: $(this).data('bio'),
        };
        var urlParams = $.param(params);

        // Load the popup HTML using AJAX
        $.get('/tutor_bio_edit?' + urlParams, function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
            // Add the modified HTML to the modal container and show the modal
            $('#tutor-bio-edit-modal-container').html($modal);
            $('#tutorBioEditModal').modal('show');
        });
    }

    // Event binding for button click
    $('.time-slot').click(show_appt);
    $('.view-cancel').click(show_appt);
    $('.tutor-overview-btn').click(show_tutor_overview);
    $('.weekly-summary-btn').click(show_weekly_summary);
    $('.edit-tutor-bio').click(show_tutor_bio_edit);
    $('.add-time').click(add_appt_time);
});
