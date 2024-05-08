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

    function show_prev_week() {
        // Load the popup HTML using AJAX
        $.get('/prev_week', function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
            // Add the modified HTML to the modal container and show the modal
            $('#summary-modal-container').html($modal);
            $('#summaryModal').modal('show');
        });
    }

    function show_add_users() {
        // Load the popup HTML using AJAX
        $.get('/add_users', function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
            // Add the modified HTML to the modal container and show the modal
            $('#add-users-modal-container').html($modal);
            $('#addUsersModal').modal('show');
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


    function show_student_ids(){
       
        var urlParams = $.param({});

        $.get('/get_student_ids?' + urlParams, function(html) {
            var $modal = $(html);

            $('#student-id-modal-container').html($modal);
            $('#studentIdModal').modal('show');
        });

    }

    function show_tutor_ids(){
       
        var urlParams = $.param({});

        $.get('/get_tutor_ids?' + urlParams, function(html) {
            var $modal = $(html);

            $('#tutor-id-modal-container').html($modal);
            $('#tutorIdModal').modal('show');
        });

    }

    function show_admin_ids(){
       
        var urlParams = $.param({});

        $.get('/get_admin_ids?' + urlParams, function(html) {
            var $modal = $(html);

            $('#admin-id-modal-container').html($modal);
            $('#adminIdModal').modal('show');
        });

    }

    function show_copy_confirmation() {
        var params = {
            min_date: $(this).data('mindate'),
            max_date: $(this).data('maxdate'),
        };
        var urlParams = $.param(params);

        // Load the popup HTML using AJAX
        $.get('/confirm_copy_times?' + urlParams, function(html) {
            // Create a jQuery object from the HTML string
            var $modal = $(html);
            // Add the modified HTML to the modal container and show the modal
            $('#copy-times-confirm-container').html($modal);
            $('#confirmCopyModal').modal('show');
        });
    }

    // Event binding for button click
    $('.time-slot').click(show_appt);
    $('.view-cancel').click(show_appt);
    $('.tutor-overview-btn').click(show_tutor_overview);
    $('.weekly-summary-btn').click(show_weekly_summary);
    $('.prev-week-btn').click(show_prev_week);
    $('.add-users-btn').click(show_add_users);
    $('.edit-tutor-bio').click(show_tutor_bio_edit);
    $('.choose_netid').click(show_student_ids);
    $('.choose_netid_tutor').click(show_tutor_ids);
    $('.choose_netid_admin').click(show_admin_ids);
    $('.add-time').click(add_appt_time);
    $('.copy-times').click(show_copy_confirmation);
});
