#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Anaika Mehra
#-----------------------------------------------------------------------
import os
import time
import flask
import db_queries
import db_modify
from datetime import date
#-----------------------------------------------------------------------
today = date.today()
# get_cur_appointment() -> list of scheduled appointments + tutor + comments 
def get_cur_appoinment1(coursenum):
    curr_appointments = []
    all_appointments = db_queries.getAppointments(coursenum)
    for row in all_appointments:
        if (row[0] > today or row[0].date == today) and row[1] == True:
            curr_appointments.append(row[0])
    return curr_appointments
#-----------------------------------------------------------------------
def get_cur_appoinment2(coursenum):
    curr_appointments = db.get_appointments({"start_time": today, "booked": True})
    return curr_appointments
#----------------------------------------------------------------------- 

# add_appoinment()/delete_appointment/modify_appointment() -> modify results from get_cur_appoinment()
# get_times() -> return list of available times + scheduled studentIDs;
def get_times_students():
    available_appointments = db.get_appointments({"start_time": today, "booked": False})
    times = []
    for row in available_appointments:
        times.append(row[0], row[3])
    return times
#----------------------------------------------------------------------- 

def get_appointment_details(studentnetID):
    curr_appointments = db.get_appointments({"student": studentnetID, "booked":True})
    return curr_appointments
#----------------------------------------------------------------------- 

# delete_appointment/modify_appointment() 
def edit_appointment(oldtime, newtime, tutornetID, action):
    if action == "delete":
        db.modify.cancel_appointment(oldtime, tutornetID)
    else:
        appt_details = db.get_appointments({"start_time": oldtime, "booked": True, "tutor" = tutornetID})
        db.modify.cancel_appointment(oldtime, tutornetID)
        db.modify.add_appoinment(newtime, tutornetID)
#----------------------------------------------------------------------- 