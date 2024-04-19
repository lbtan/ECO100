$(document).ready(function(){

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
        
        var prevWeekNum = parseInt(week) - 1;
        var prevWeekButton = document.getElementById('prev-week');
        prevWeekButton.setAttribute('data-week', prevWeekNum);
        prevWeekButton.disabled = prevWeekNum < 0 || prevWeekNum > calendars.length - 1 ? true : false;
        
        var nextWeekNum = parseInt(week) + 1;
        var nextWeekButton = document.getElementById('next-week');
        nextWeekButton.setAttribute('data-week', nextWeekNum);
        nextWeekButton.disabled = nextWeekNum < 0 || nextWeekNum > calendars.length - 1 ? true : false;
    };
    
    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener('click', showCalendar, false);
    }

    document.getElementById("calendar-0").style.display = "block";
});
