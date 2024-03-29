#!/usr/bin/env python

#-----------------------------------------------------------------------
# db_modify.py
# Author: Hita Gupta
#-----------------------------------------------------------------------

import sys
import os
import datetime
import sqlalchemy
import sqlalchemy.orm
import dotenv
from . import database

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

                session.commit()
        
        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

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

            session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def add_appointment(time, tutor_netid):

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
                                               tutor_netid=tutor_netid)
            
            session.add(appointment)

            session.commit()

        _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

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
                session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

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

                session.commit()

        finally:
            _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

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

            session.commit()

        _engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

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
    #cancel_appointment(datetime.datetime(2024, 3, 14, 9, 30), 'tu111')

    # this time is booked
    cancel_appointment(datetime.datetime(2025, 3, 26, 15, 30), 'hgranger')

def _test_add_appointment():
    # this already exists in the table
    #add_appointment(datetime.datetime(2024, 3, 16, 9, 30), 'tu222')
    
    # this time is not in the table
    add_appointment(datetime.datetime(2024, 3, 25, 9, 30), 'tu222')

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
    #_test_book_appointment()
    _test_cancel_appointment()
    #_test_add_appointment()
    #_test_delete_appointment()
    #_test_update_tutor_bio()
    #_test_add_user()

if __name__ == '__main__':
    _test()