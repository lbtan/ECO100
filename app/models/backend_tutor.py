#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Anaika Mehra
#-----------------------------------------------------------------------
import os
import time
import flask
from . import db_queries
from . import db_modify
import datetime 
#-----------------------------------------------------------------------
today = datetime.date.today()
today_test = datetime.datetime(2024, 1, 1)

# get_times() -> return list of available times starting today +  tutornetID; 
def get_times_tutors():
    available_appointments = db_queries.get_appointments({"start_time": today})
    if available_appointments[0] == False:
        return available_appointments
    times = []
    for row in available_appointments:
        # times.append(row[0], row[2])
        times.append((row._time, row._tutor_netid, row._booked, row._student_netid))
    return times

#-----------------------------------------------------------------------
# get_cur_appointment() -> list of scheduled appointments + tutor + comments 
# can add coursenum as parameter later
def get_cur_appoinments():
    curr_appointments = db_queries.get_appointments({"start_time": today_test, "booked": True})
    if curr_appointments[0] == False:
        return curr_appointments
    appointments = []
    for row in curr_appointments:
        appointments.append((row._time, row._tutor_netid, row._comments))
    return appointments
#----------------------------------------------------------------------- 
# add_times() -> edit all available times; 
# get_appointment_details() -> get details of current appointment;
def get_appointment_details(tutornetID):
    curr_appointments = db_queries.get_appointments({"tutor": tutornetID, "booked":True})
    print(curr_appointments)
    return curr_appointments
    # can return more specfic things using 
    # return [curr_appointments._tutor_netid, curr_appointments.start_time]
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