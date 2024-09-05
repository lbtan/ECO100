#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Anaika Mehra
#-----------------------------------------------------------------------
from . import db_queries
from . import db_modify
import datetime 
from . import date

#-----------------------------------------------------------------------

# get_times() -> return list of available times starting now +  tutornetID; 
def get_times_tutors():
    available_appointments = db_queries.get_appointments({"start_time": date.now()})
    if len(available_appointments) > 0 and available_appointments[0] == False:
        return available_appointments
    times = []
    for row in available_appointments:
        # times.append(row[0], row[2])
        times.append((row.get_time(), row.get_tutor_netid(), row.get_booked(), row.get_student_netid()))
    return times

def get_prev_times(tutor):
    available_appointments = db_queries.get_appointments({"tutor_netid": tutor, "end_time": date.now() - datetime.timedelta(minutes=1)})
    if len(available_appointments) > 0 and available_appointments[0] == False:
        return available_appointments
    times = []
    for row in available_appointments:
        # times.append(row[0], row[2])
        times.append((row.get_time(), row.get_tutor_netid(), row.get_booked(), row.get_student_netid(), row.get_show()))
    sorted_appointments = sorted(times, key=lambda x: x[0])
    return sorted_appointments

#-----------------------------------------------------------------------
# get_cur_appointment() -> list of scheduled appointments + tutor + comments 
# can add coursenum as parameter later
def get_cur_appoinments():
    curr_appointments = db_queries.get_appointments({"start_time": date.now(), "booked": True})
    if len(curr_appointments) > 0 and curr_appointments[0] == False:
        return curr_appointments
    appointments = []
    for row in curr_appointments:
        appointments.append((row.get_time(), row.get_tutor_netid(), row.get_comments()))
    return appointments
#----------------------------------------------------------------------- 
# add_times() -> edit all available times; 
# get_appointment_details() -> get details of current appointment;
def get_appointment_details(tutornetID):
    curr_appointments = db_queries.get_appointments({"tutor_netid": tutornetID, "booked":True})
    print(curr_appointments)
    return curr_appointments
    # can return more specfic things using 
    # return [curr_appointments._tutor_netid, curr_appointments.start_time]
#----------------------------------------------------------------------- 
# copy times from previous week
def copy_prev_week_times(min_date, max_date, tutor_netid):
    # Delete existing times for this week
    future_appointments = db_queries.get_appointments({"tutor_netid": tutor_netid, "start_time": min_date, "end_time": max_date, "booked": False})
    for appointment in future_appointments:
        db_modify.delete_appointment(appointment.get_time(), appointment.get_tutor_netid())
    prev_appointments = db_queries.get_appointments({"tutor_netid": tutor_netid, "start_time": min_date - datetime.timedelta(days=7), "end_time": max_date - datetime.timedelta(days=6)})
    for appointment in prev_appointments:
        new_time = appointment.get_time() + datetime.timedelta(days=7)
        db_modify.add_appointment(new_time, appointment.get_tutor_netid())

#----------------------------------------------------------------------- 
# handled in student
# # delete_appointment/modify_appointment() 
# def edit_appointment(oldtime, newtime, tutornetID, action):
#     if action == "delete":
#         db.modify.cancel_appointment(oldtime, tutornetID)
#     else:
#         appt_details = db.get_appointments({"start_time": oldtime, "booked": True, "tutor": tutornetID})
#         db.modify.cancel_appointment(oldtime, tutornetID)
#         db.modify.add_appoinment(newtime, tutornetID)
#----------------------------------------------------------------------- 
def main():
    tutor_appointment = get_appointment_details("tu111")
    print(tutor_appointment)
    for row in tutor_appointment:
        print(row._time)
    # curr_appointment = get_cur_appoinments()
    # print(curr_appointment)


#----------------------------------------------------------------------- 
if __name__ == '__main__':
    main()