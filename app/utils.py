#-----------------------------------------------------------------------
# utils.py
# Authors: Libo Tan
# 
#
# 
#-----------------------------------------------------------------------

from collections import defaultdict
import datetime

#-----------------------------------------------------------------------

def appointments_by_tutor(appointments, userId):
    """
    
    Parses db input appointments for html code, return all booked appointments for userId in 
    chronological order.

    (used GPT to look up useful functions like defaultdict() and strftime())
    """
    tutor_appointments = []
    for appt_time, tutor_netid, booked, student_netid in appointments:
        if booked and tutor_netid == userId:
            formatted_date = appt_time.strftime('%Y-%m-%d')  
            formatted_time = appt_time.strftime('%I:%M %p')  
            tutor_appointments.append((formatted_date, formatted_time, student_netid))
    sorted_appointments = sorted(tutor_appointments, key=lambda x: x[0])
    return sorted_appointments


def appointments_by_time(appointments):
    """
    
    Sort appointments by time. (used gpt for lambda functions)
    """
    sorted_appointments = sorted(appointments, key=lambda x: x[0])
    appointments_by_date = defaultdict(lambda: defaultdict(list))
    for appt_time, tutor_netid, booked, student_netid in sorted_appointments:
        date_key = appt_time.date()
        time_str = appt_time.strftime('%I:%M %p')
        appointments_by_date[date_key][tutor_netid].append((time_str, booked))
    
    return appointments_by_date


