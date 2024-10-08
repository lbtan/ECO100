#!/usr/bin/env python

#-----------------------------------------------------------------------
# db_modify.py
# Author: Hita Gupta and Sofia Marina
#-----------------------------------------------------------------------

import sys
import os
import datetime
import sqlalchemy
import sqlalchemy.orm
import dotenv
from . import database
# import database 

#-----------------------------------------------------------------------

dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

def book_appointment(time, tutor_netid, student_netid, comments, 
                     coursenum):

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        try:

            with sqlalchemy.orm.Session(_engine) as session:

                query = (session.query(database.Appointment)
                    .filter(database.Appointment.tutor_netid == 
                            tutor_netid)
                    .filter(database.Appointment.time == time))

                row = query.one()
                if row.booked:
                    raise Exception(("Appointment at {} with {} is " +
                                    "booked already").format(time, 
                                    tutor_netid))

                row.booked = True
                row.student_netid = student_netid
                row.comments = comments
                row.coursenum = coursenum

                print("{} booked appointment at {} with {}".format(student_netid, time, tutor_netid))

                session.commit()
        
        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        return False, ex
    
    return True, True

def cancel_appointment(time, tutor_netid):

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        try:

            with sqlalchemy.orm.Session(_engine) as session:

                query = (session.query(database.Appointment)
                    .filter(database.Appointment.tutor_netid == 
                            tutor_netid)
                    .filter(database.Appointment.time == time))

                row = query.one()
                if not row.booked:
                    raise Exception(("Appointment at {} with {} is " +
                                    "not booked").format(time, 
                                    tutor_netid))

                row.booked = False
                row.student_netid = None
                row.comments = None
                row.coursenum = None

                print("Appointment at {} with {} is cancelled".format(time, tutor_netid))

                session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

def add_appointment(time, tutor_netid, location):

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        with sqlalchemy.orm.Session(_engine) as session:

            # check if this appointment already exists
            query = (session.query(database.Appointment)
                .filter(database.Appointment.tutor_netid == tutor_netid)
                .filter(database.Appointment.time == time))
            
            if query.count() > 0:
                _engine.dispose()
                raise Exception(("Appointment at {} with {} already " +
                                "exists").format(time, tutor_netid))
            
            appointment = database.Appointment(time=time, 
                                               booked=False, 
                                               tutor_netid=tutor_netid,
                                               location=location)
            
            session.add(appointment)

            print("Appointment at {} with {} added. Location is {}".format(time, tutor_netid, location))

            session.commit()

        _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

def modify_appointment_time(prev_time, new_time, tutor_netid):
    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        try:
            with sqlalchemy.orm.Session(_engine) as session:

                # check if appointment at new time already exists
                query_new = (session.query(database.Appointment)
                    .filter(database.Appointment.tutor_netid == tutor_netid)
                    .filter(database.Appointment.time == new_time))
                
                if query_new.count() > 0:
                    _engine.dispose()
                    raise Exception(("Appointment at {} with {} already " +
                                    "exists").format(new_time, tutor_netid))
                
                # check for existing appointment at old time
                query_prev = (session.query(database.Appointment)
                    .filter(database.Appointment.tutor_netid == tutor_netid)
                    .filter(database.Appointment.time == prev_time))
                
                if query_prev.count() == 0:
                    raise Exception(("Appointment at {} with {} does" +
                                    "not exist").format(prev_time, tutor_netid))
                
                appointment = query_prev.one()
                appointment.time = new_time

                print("Appointment at {} with {} has new time {}".format(prev_time, tutor_netid, new_time))

                session.commit()
        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

def delete_appointment(time, tutor_netid):

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        try:

            with sqlalchemy.orm.Session(_engine) as session:

                query = (session.query(database.Appointment)
                    .filter(database.Appointment.tutor_netid == 
                            tutor_netid)
                    .filter(database.Appointment.time == time))

                row = query.one() # ensure the appointment time exists
            
                session.delete(row)

                print("Appointment at {} with {} deleted".format(time, tutor_netid))
                7
                session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

def update_tutor_bio(tutor_netid, bio):

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        try:

            with sqlalchemy.orm.Session(_engine) as session:

                query = session.query(database.Tutor).filter(
                    database.Tutor.netid == tutor_netid
                )

                row = query.one()
                row.bio = bio

                print("Tutor {} bio updated".format(tutor_netid))

                session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

def update_showed_up(tutor_netid, time, showed_up):

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        try:

            with sqlalchemy.orm.Session(_engine) as session:
                query = session.query(database.Appointment).filter(
                    database.Appointment.tutor_netid == tutor_netid
                ).filter(
                    database.Appointment.time == time
                )

                row = query.one()
                row.showed_up = showed_up

                print("Tutor {} marked showed up status for appointment at {} to {}".format(tutor_netid, time, showed_up))

                session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

def add_user(netid, user_type, coursenum, name):

    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        with sqlalchemy.orm.Session(_engine) as session:

            # check if this user already exists
            query = (session.query(database.User)
                .filter(database.User.netid == netid)
                .filter(database.User.user_type == user_type)
                .filter(database.User.coursenum == coursenum))
                        
            if query.count() > 0:
                _engine.dispose()
                raise Exception(("User with netid {}, user type {}, " +
                                 "coursenum {} and name {} already " + 
                                 "exists").format(netid, user_type, 
                                 coursenum, name))
            
            user = database.User(netid=netid, name=name, user_type=
                                 user_type, coursenum=coursenum)
            
            session.add(user)

            if user_type == "tutor":
                tutor = database.Tutor(netid=netid, bio="")
                session.add(tutor)

            print("User with netid {}, user type {}, coursenum {} and name {} added".format(netid, user_type, coursenum, name))
            session.commit()

        _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

def delete_user(netid, user_type):
    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        try:

            with sqlalchemy.orm.Session(_engine) as session:

                user_query = (session.query(database.User)
                    .filter(database.User.netid == netid)
                    .filter(database.User.user_type == user_type))
                row = user_query.one() # ensure the user exists
            
                session.delete(row)

                if user_type == 'student':
                    appt_query = (session.query(database.Appointment)
                                  .filter(database.Appointment.student_netid == netid))
                    table = appt_query.all() 

                    for row in table:
                        session.delete(row)

                elif user_type == 'tutor':
                    appt_query = (session.query(database.Appointment)
                                  .filter(database.Appointment.tutor_netid == netid))
                    table = appt_query.all() 

                    for row in table:
                        session.delete(row)

                    delete_tutor(netid)

                print("User with netid {} and user_type {} deleted".format(netid, user_type))

                session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

def delete_tutor(netid):
    try:
        _engine = sqlalchemy.create_engine(_DATABASE_URL)

        try:

            with sqlalchemy.orm.Session(_engine) as session:

                query = (session.query(database.Tutor)
                    .filter(database.Tutor.netid == netid))
                row = query.one() # ensure the user exists
            
                session.delete(row)

                print("Tutor with netid {} deleted".format(netid))

                session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)

#-----------------------------------------------------------------------

# For testing:

def _test_book_appointment():
    # this time does not exist
    #book_appointment(datetime.datetime(2024, 3, 21, 9, 30), 'tu111', 
    #                 'st111', 'none')
    
    # this time is booked
    #book_appointment(datetime.datetime(2024, 3, 18, 9, 30), 'tu111', 
    #                 'st111', 'none')
    
    # this time is available
    book_appointment(datetime.datetime(2024, 3, 16, 9, 30), 'tu222',
                     'st111', 'none')

def _test_cancel_appointment():
    # this time does not exist
    #cancel_appointment(datetime.datetime(2024, 3, 21, 9, 30), 'tu111')

    # this time is not booked
    #cancel_appointment(datetime.datetime(2025, 3, 24, 16, 0), 'pweasley')

    # this time is booked
    cancel_appointment(datetime.datetime(2025, 3, 26, 15, 30), 'hgranger')

def _test_add_appointment():
    # this already exists in the table
    #add_appointment(datetime.datetime(2024, 3, 16, 9, 30), 'tu222')
    
    # this time is not in the table
    add_appointment(datetime.datetime(2024, 3, 25, 9, 30), 'tu222', 'whitman common room')

def _test_delete_appointment():
    # this is not in the table
    #delete_appointment(datetime.datetime(2024, 3, 25, 9, 30), 'tu333')

    # this is in the table
    delete_appointment(datetime.datetime(2024, 3, 14, 9, 30), 'tu111')

def _test_update_tutor_bio():
    # this tutor doesn't exist
    #update_tutor_bio('tu444', 'New MyBio 4')

    # this tutor exists
    update_tutor_bio('tu111', 'New MyBio 1')

def _test_add_user():
    # this user already exists
    add_user("st333", "student", "1", "Student Three")

def _test():
    """
    
    Unit tests for db_modify.py. Each function tests a specific 
    functionality of database modifying operations and prints the 
    outcome for debugging purposes.
    
    
    """
    _test_book_appointment()
    _test_cancel_appointment()
    _test_add_appointment()
    _test_delete_appointment()
    _test_update_tutor_bio()
    _test_add_user()
    
if __name__ == '__main__':
    _test()