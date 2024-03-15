#!/usr/bin/env python

#-----------------------------------------------------------------------
# db_queries.py
# Author: Hita Gupta, ECO 100 Tutoring App Team
#-----------------------------------------------------------------------

import sys
import os
import datetime
import sqlalchemy
import sqlalchemy.orm
import dotenv
import user as usermod
import appointment as appointmentmod
import database

#-----------------------------------------------------------------------

dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

def get_appointments(props={}):
    appts = []

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        with sqlalchemy.orm.Session(_engine) as session:

            query = session.query(database.Appointment)
            
            if "coursenum" in props:
                query = query.filter(
                    database.Appointment.coursenum == props["coursenum"]
                )

            if "start_time" in props:
                query = query.filter(
                    database.Appointment.time >= props['start_time']
                )

            if "end_time" in props:
                # add one day so that date comparison is inclusive
                end_time = props["end_time"] + datetime.timedelta(
                    days=1
                )

                query = query.filter(
                    database.Appointment.time <= end_time
                )
            
            if "student_netid" in props:
                query = query.filter(
                    database.Appointment.student_netid == 
                        props["student_netid"]
                )
            
            if "tutor_netid" in props:
                query = query.filter(
                    database.Appointment.tutor_netid == props[
                        "tutor_netid"
                    ]
                )
            
            if "booked" in props:
                query = query.filter(
                    database.Appointment.booked.is_(props["booked"])
                )
            
            table = query.all()
            for row in table:
                appt = appointmentmod.Appointment(row.time, 
                                                row.booked, 
                                                row.tutor_netid, 
                                                row.student_netid, 
                                                row.comments, 
                                                row.coursenum)
                appts.append(appt)

        _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

    return appts

def get_user_info(props={}):    
    users = []

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        with sqlalchemy.orm.Session(_engine) as session:

            query = session.query(database.User)

            if "netid" in props:
                query = query.filter(
                    database.User.netid == props["netid"]
                )
            
            if "name" in props:
                query = query.filter(
                    database.User.name.ilike("%" + props["name"] + "%")
                )

            if "user_type" in props:
                query = query.filter(
                    database.User.user_type == props["user_type"]
                )

            if "coursenum" in props:
                query = query.filter(
                    database.User.coursenum == props["coursenum"]
                )
                    
            table = query.all()
            for row in table:
                user = usermod.User(row.netid, row.name, row.user_type, 
                                    row.coursenum)
                users.append(user)

        _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

    return users

def get_tutor_bio(tutor_netid):

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        with sqlalchemy.orm.Session(_engine) as session:

            query = session.query(database.Tutor).filter(
                database.Tutor.netid == tutor_netid
            )

            try:
                row = query.one()
            except Exception as ex:
                _engine.dispose()
                print(ex, file=sys.stderr)
                sys.exit(1)

        _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

    return row.bio

#-----------------------------------------------------------------------

# For testing:

def _test_get_appointments():
    appointments = get_appointments()
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"coursenum": '1'})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"start_time": 
                                     datetime.date(2024, 3, 14)})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"start_time": 
                                     datetime.date(2024, 3, 16)})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"end_time": 
                                     datetime.date(2024, 3, 14)})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"end_time": 
                                     datetime.date(2024, 3, 16)})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"tutor_netid": "tu111"})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"student_netid": "st111"})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"student_netid": "st222"})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"booked": True})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"booked": False})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

    appointments = get_appointments({"coursenum": "1", "booked": False})
    for appt in appointments:
        print(appt.to_tuple())
        print()
    print("---------------------------------")

def _test_get_user_info():
    query = {}
    print(query)
    users = get_user_info(query)
    for user in users:
        print(user.to_tuple())
        print()
    print("---------------------------------")

    query = {"user_type": "student"}
    print(query)
    users = get_user_info(query)
    for user in users:
        print(user.to_tuple())
        print()
    print("---------------------------------")

    query = {"coursenum": "1"}
    print(query)
    users = get_user_info(query)
    for user in users:
        print(user.to_tuple())
        print()
    print("---------------------------------")

    query = {"coursenum": "1", "user_type": "tutor"}
    print(query)
    users = get_user_info(query)
    for user in users:
        print(user.to_tuple())
        print()
    print("---------------------------------")

    query = {"name": "stude"}
    print(query)
    users = get_user_info(query)
    for user in users:
        print(user.to_tuple())
        print()
    print("---------------------------------")

def _test_get_tutor_bio():
    netid = 'tu111'
    print(netid)
    bio = get_tutor_bio(netid)
    print(bio + "\n")
    print("---------------------------------")

    netid = ''
    print(netid)
    bio = get_tutor_bio(netid)
    print(bio + "\n")
    print("---------------------------------")

def _test():
    #_test_get_appointments()
    #_test_get_user_info()
    _test_get_tutor_bio()

if __name__ == '__main__':
    _test()