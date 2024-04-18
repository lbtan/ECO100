#-----------------------------------------------------------------------
# utils.py
# Authors: Libo Tan and Sofia Marina
# 
#
# 
#-----------------------------------------------------------------------

from collections import defaultdict
from collections import Counter
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
            formatted_date = appt_time.date()
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

def appointments_by_student(appointments, studentId):
    """
    Parses db input appointments for html code, return all booked appointments for studentId in 
    chronological order. (adapted from Angela's code)
    """
    student_appointments = []
    for time, student_netid, tutor_netid, comments in appointments:
        if student_netid == studentId:
            formatted_date = time.date()
            formatted_time = time.strftime('%I:%M %p')
            student_appointments.append((formatted_date, formatted_time, tutor_netid))
    sorted_appointments = sorted(student_appointments, key=lambda x: x[0])
    return sorted_appointments

def available_appointments_by_time(appointments, booked_appts):
    """
    Parses db input appointments for html code, return all unbooked appointments  
    in chronological order for each tutor. (adapted from Angela's code)
    """ 
    # tutors can only have 8 hours a week
    tutor_appt_counts = Counter(tutor for _, _, tutor, _ in booked_appts)
    sorted_appointments = sorted(appointments, key=lambda x: x[0])
    appointments_by_date = defaultdict(lambda: defaultdict(list))
    for appt_time, student, tutor in sorted_appointments:
        if tutor_appt_counts[tutor] > 8:
            continue
        date_key = appt_time.date()
        time_str = appt_time.strftime('%I:%M %p')
        appointments_by_date[date_key][tutor].append(time_str)
    
    return appointments_by_date

def group_by_week(appointments):
    """
    Given a list of appointments for each date, returns them
    chronologically grouped by week. (Hita)
    """
    weekly_appointments = defaultdict(lambda: defaultdict(list))
    for date, appts in appointments.items():
        week = date.isocalendar()[:2] # https://stackoverflow.com/questions/29260224/how-to-group-and-count-events-by-week
        weekly_appointments[week][date] = appts

    return weekly_appointments