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
import models.db_queries as db_queries

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
            tutor_appointments.append((appt_time, student_netid))
    sorted_appointments = sorted(tutor_appointments, key=lambda x: x[0])
    return sorted_appointments

def appointments_by_time(appointments, tutor=None):
    """
    
    Sort appointments by time. (used gpt for lambda functions)
    """
    sorted_appointments = sorted(appointments, key=lambda x: x[0])
    appointments_by_date = defaultdict(lambda: defaultdict(list))

    if tutor:
        last_date = None

    for appt_time, tutor_netid, booked, student_netid in sorted_appointments:
        date_key = appt_time.date()

        if tutor:
            if last_date != None and date_key > last_date + datetime.timedelta(days=1):
                curr = last_date + datetime.timedelta(days=1)
                while curr < date_key:
                    appointments_by_date[curr] = {}
                    curr += datetime.timedelta(days=1)
                
        appointments_by_date[date_key][tutor_netid].append((appt_time, booked))
        last_date = date_key
    
    # If tutor, add all dates until end of semester
    if tutor:
        last_appt_date = max(appointments_by_date)
        max_appt_date = datetime.date(year=last_appt_date.year, month=5, day=1)
        curr = last_appt_date + datetime.timedelta(days=1)
        while curr <= max_appt_date:
            appointments_by_date[curr] = {}
            curr += datetime.timedelta(days=1)

        # Sort times by tutor
        for date in appointments_by_date:
            appointments_by_date[date] = dict(sorted(appointments_by_date[date].items(), key=lambda x: (0, x[0]) if x[0] == tutor else (1, x[0])))
    else:
        for date in appointments_by_date:
            appointments_by_date[date] = dict(sorted(appointments_by_date[date].items(), key=lambda x: x[0]))

    return appointments_by_date

def appointments_by_student(appointments, studentId):
    """
    Parses db input appointments for html code, return all booked appointments for studentId in 
    chronological order. (adapted from Angela's code)
    """
    student_appointments = []
    for time, student_netid, tutor_netid, comments in appointments:
        if student_netid == studentId:
            student_appointments.append((time, tutor_netid))
    sorted_appointments = sorted(student_appointments, key=lambda x: x[0])
    return sorted_appointments

def available_appointments_by_time(appointments, booked_appts):
    """
    Parses db input appointments for html code, return all unbooked appointments  
    in chronological order for each tutor. (adapted from Angela's code)
    """ 
    # tutors can only have 8 hours a week
    tutor_appt_counts = defaultdict(lambda: defaultdict(int))
    for appt in booked_appts:
        tutor_appt_counts[appt[0].isocalendar()[:2]][appt[2]] += 1

    sorted_appointments = sorted(appointments, key=lambda x: x[0])
    appointments_by_date = defaultdict(lambda: defaultdict(list))

    for appt_time, student, tutor in sorted_appointments:
        if tutor_appt_counts[appt_time.isocalendar()[:2]][tutor] > 8:
            continue
        date_key = appt_time.date()
        appointments_by_date[date_key][tutor].append(appt_time)
    
    for date in appointments_by_date:
        appointments_by_date[date] = dict(sorted(appointments_by_date[date].items(), key=lambda x: x[0]))

    return appointments_by_date

def group_by_week(appointments):
    """
    Given a list of appointments for each date, returns them
    chronologically grouped by week. (Hita)
    """
    weekly_appointments = []
    weeks = set()
    for date, appts in appointments.items():
        week = date.isocalendar()[:2] # https://stackoverflow.com/questions/29260224/how-to-group-and-count-events-by-week
        
        # if this date is in a new week, then create a new dictionary
        if week not in weeks:
            weekly_appointments.append({})
        weekly_appointments[-1][date] = appts
        
        weeks.add(week) # this week has been seen

    return weekly_appointments

def get_tutor_ids():
    """
    Get all tutor ids in database
    """
    tutor_ids = []
    user_ids = db_queries.get_user_info(props={"user_type": "tutor"})
    for user_id in user_ids:
        tutor_ids.append(user_id.get_netid())
    return tutor_ids

def get_student_ids():
    """
    
    Get all tutor id in database
    """

    tutor_ids = []
    user_ids = db_queries.get_user_info(props={"user_type": "student"})
    for user_id in user_ids:
        tutor_ids.append(user_id.get_netid())
    return tutor_ids


def get_admin_ids():
    """
    
    Get all tutor id in database
    """

    tutor_ids = []
    user_ids = db_queries.get_user_info(props={"user_type": "admin"})
    for user_id in user_ids:
        tutor_ids.append(user_id.get_netid())
    return tutor_ids

def get_names():
    users = db_queries.get_user_info({"coursenum": "1"})
    return {user.get_netid(): user.get_name() for user in users}

def get_can_book(cur_appointments, weekly_appointments):
    cur_appointments_weeks = set([appt[0].isocalendar()[:2] for appt in cur_appointments])
    
    can_book = [True] * len(weekly_appointments)
    for i in range(len(weekly_appointments)):
        week = next(iter(weekly_appointments[i])).isocalendar()[:2]
        if week in cur_appointments_weeks:
            can_book[i] = False
    
    return can_book