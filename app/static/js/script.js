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

    // https://stackoverflow.com/questions/19655189/javascript-click-event-listener-on-class
    var elements = document.getElementsByClassName("update-week-calendar");

    var showCalendar = function() {
        var week = this.getAttribute("data-week");
        var calendar = document.getElementById("calendar-" + week);

        calendar.style.display = "block";

        // hide other calendars
        // https://stackoverflow.com/questions/10111668/find-all-elements-whose-id-begins-with-a-common-string
        var calendars = document.querySelectorAll('[id^="calendar-"]');
        console.log(calendars);
        for (var i = 0; i < calendars.length; i++) {
            if (calendars[i].id != "calendar-" + week) {
                calendars[i].style.display = "none";
            }
        }

        var prevWeekButton = document.getElementById('prev-week');
        prevWeekButton.setAttribute('data-week', parseInt(week) - 1);
        var nextWeekButton = document.getElementById('next-week');
        nextWeekButton.setAttribute('data-week', parseInt(week) + 1); 
    };
    
    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener('click', showCalendar, false);
    }

    document.getElementById("calendar-0").style.display = "block";

    // Event binding for button click
    $('.time-slot').click(show_appt);
    $('.view-cancel').click(show_appt);
    $('.tutor-overview-btn').click(show_tutor_overview);
    $('.weekly-summary-btn').click(show_weekly_summary);
    $('.edit-tutor-bio').click(show_tutor_bio_edit);
});
