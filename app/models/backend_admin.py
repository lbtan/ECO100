#!/usr/bin/env python

#-----------------------------------------------------------------------
# backend_admin.py
# Author: Hita Gupta
#-----------------------------------------------------------------------

import pandas as pd
from . import db_queries
from . import db_modify
import datetime

def import_users(csv_path, user_type, coursenum):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        try:
            name = row['Name']
            netid = row['Netid']
            if type(name) != str or len(netid) > 15:
                continue
            db_modify.add_user(netid, user_type, coursenum, name)
        except:
            return 'Error', 'Unable to process. Please make sure your file contains two columns, Name and Netid.'
    
    return 'Upload Confirmation', 'Succesfully uploaded and processed file.'

def weekly_summary(coursenum, today=datetime.date.today()):
    week_before = today - datetime.timedelta(days=7)
    appts = db_queries.get_appointments({"start_time": week_before, 
                                         "end_time": today,
                                         "booked": True,
                                         "coursenum": coursenum})
    if appts[0] == False:
        return False
    
    summary = {}
    summary["Total Appointments"] = len(appts)

    tutors = db_queries.get_user_info({"user_type": "tutor",
                                       "coursenum": coursenum})
    if tutors[0] == False:
        return False

    appts_by_tutor = {tutor.get_netid(): 0 for tutor in tutors}
    for appt in appts:
        appts_by_tutor[appt.get_tutor_netid()] += 1
    
    tutor_names = {tutor.get_netid(): tutor.get_name() for tutor in 
                   tutors}
    appts_by_tutor = {tutor_names[netid]: appts_by_tutor[netid] for 
                      netid in appts_by_tutor}
    
    summary["Total Appointments (By Tutor)"] = appts_by_tutor

    return summary

#-----------------------------------------------------------------------

def _test():
    #import_users("netid.csv", "student", "1")
    print(weekly_summary("1"))

if __name__ == '__main__':
    _test()