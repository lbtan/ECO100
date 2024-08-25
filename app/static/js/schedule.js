$(document).ready(function(){

    var showCalendar = function(week) {
        var calendar = document.getElementById("calendar-" + week);

        calendar.style.display = "block";

        // hide other calendars
        // https://stackoverflow.com/questions/10111668/find-all-elements-whose-id-begins-with-a-common-string
        var calendars = document.querySelectorAll('[id^="calendar-"]');
        for (var i = 0; i < calendars.length; i++) {
            if (calendars[i].id != "calendar-" + week) {
                calendars[i].style.display = "none";
            }
        }
        
        var prevWeekNum = parseInt(week) - 1;
        var prevWeekButton = document.getElementById('prev-week');
        prevWeekButton.setAttribute('data-week', prevWeekNum);
        prevWeekButton.disabled = prevWeekNum < 0 || prevWeekNum > calendars.length - 1 ? true : false;
        
        var nextWeekNum = parseInt(week) + 1;
        var nextWeekButton = document.getElementById('next-week');
        nextWeekButton.setAttribute('data-week', nextWeekNum);
        nextWeekButton.disabled = nextWeekNum < 0 || nextWeekNum > calendars.length - 1 ? true : false;

        // Store the current week in a cookie
        $.cookie('lastSeenWeek', week, { expires: 1, path: '/' });
    };

    var showCalendarEvent = function() {
        var week = this.getAttribute("data-week");
        showCalendar(week);
    }

    // Show calendar on Previous Week/Next Week button click
    var elements = document.getElementsByClassName("update-week-calendar");
    for (var i = 0; i < elements.length; i++) {
        // https://stackoverflow.com/questions/19655189/javascript-click-event-listener-on-class
        elements[i].addEventListener('click', showCalendarEvent, false);
    }
    
    // Show last seen week on page load, else show week 0 by default
    var lastSeenWeek = $.cookie('lastSeenWeek');

    let initialWeek = null;
    if (lastSeenWeek && document.getElementById("calendar-" + lastSeenWeek)) {
        initialWeek = lastSeenWeek;
    } 
    else {
        initialWeek = "0";
    }
    showCalendar(initialWeek);
});
