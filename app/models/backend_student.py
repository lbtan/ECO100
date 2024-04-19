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
# get_cur_appointment_student() -> list of scheduled appointments + tutor + student + comments 
# can add coursenum as parameter later
def get_cur_appoinments_student():
    curr_appointments = db_queries.get_appointments({"start_time": today_test, "booked": True})
    if curr_appointments[0] == False:
        return curr_appointments
    appointments = []
    for row in curr_appointments:
        appointments.append((row._time, row._student_netid, row._tutor_netid, row._comments))
    return appointments
#----------------------------------------------------------------------- 
# get_times() -> return list of available times + scheduled studentIDs;
def get_times_students():
    available_appointments = db_queries.get_appointments({"start_time": today_test, "booked": False})
    if available_appointments[0] == False:
        return available_appointments
    times = []
    for row in available_appointments:
        # times.append(row[0], row[2])
        times.append((row._time, row._student_netid, row._tutor_netid))
    return times
#----------------------------------------------------------------------- 
# add_times() -> edit all available times; 
# get_appointment_details() -> get details of current appointment;
def get_appointment_details(student_netid):
    curr_appointments = db_queries.get_appointments({"student": student_netid, "booked":True})
    print(curr_appointments)
    return curr_appointments
    # can return more specfic things using 
    # return [curr_appointments._tutor_netid, curr_appointments.start_time]
#----------------------------------------------------------------------- 

# delete_appointment/modify_appointment() 
def edit_appointment(oldtime, newtime, tutornetID, action):
    if action == "cancel":
        db_modify.cancel_appointment(oldtime, tutornetID)
    else:
        appt_details = db_queries.get_appointments({"start_time": oldtime, "booked": True, "tutor_netid": tutornetID})
        db_modify.delete_appointment(oldtime, tutornetID)
        db_modify.add_appointment(newtime, tutornetID)
#----------------------------------------------------------------------- 
def main():
#    times = get_times_students()
#    print(times)
    # appointments = get_cur_appoinments_student()
    # print(appointments)
    appointments = get_appointment_details("st111")
    for row in appointments:
        print(row._time)
        print(row._tutor_netid)
        print(row._student_netid)
    dt = datetime.datetime(2024, 3, 16, 9, 30)
    dt_new = datetime.datetime(2024, 3, 17, 10, 30)
    # dt = 2024-03-14 09:30:00 
    # edit_appointment(dt, None, "tu111", "delete")
    edit_appointment(dt, dt_new, "tu222", None)
if __name__ == '__main__':
    main()