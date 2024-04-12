#!/usr/bin/env python

#-----------------------------------------------------------------------
# db_create.py
# Author: Hita Gupta
#-----------------------------------------------------------------------

import os
import sys
import sqlalchemy
import sqlalchemy.orm
import dotenv
import database
import datetime

# dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------


def add_user(netid, name, user_type, coursenum, session):
    """
    
    Functions that help with adding to database
    """
    user = database.User(netid=netid, name=name, user_type=user_type, coursenum=coursenum)
    session.add(user)
    return

#-----------------------------------------------------------------------
    

def add_appointment(session, time, tutor_netid, booked=False, student_netid=None, comments=None, coursenum=None):
    """
    
    Functions that help with adding to database
    """
    
    appointment = database.Appointment(time=time, booked=booked, tutor_netid=tutor_netid,
                                       student_netid=student_netid, comments=comments, coursenum=coursenum)
    session.add(appointment)
    return

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)
        sys.exit(1)

        engine = sqlalchemy.create_engine(_DATABASE_URL)

        database.Base.metadata.drop_all(engine)
        database.Base.metadata.create_all(engine)

        with sqlalchemy.orm.Session(engine) as session:

        #-----------------------------------------------------------
            
           # Define the base information for new students
            # Students
            student_base_info = [
                ('hpotter', 'Harry Potter'),
                ('rweasley', 'Ron Weasley'),
                ('ldraco', 'Draco Malfoy'),
                ('nlongbottom', 'Neville Longbottom'),
                ('gweasley', 'Ginny Weasley'),
                ('fweasley', 'Fred Weasley'),
                ('gweasley2', 'George Weasley'),
                ('cchang', 'Cho Chang'),
                ('ppatil', 'Padma Patil'),
                ('ppatil2', 'Parvati Patil')
            ]
            for netid, name in student_base_info:
                add_user(netid, name, 'student', '1',session)

            # Tutors
            tutors_info = [
                ('hgranger', 'Hermione Granger'),
                ('llvgd', 'Luna Lovegood'),
                ('pweasley', 'Percy Weasley')
            ]
            for netid, name in tutors_info:
                add_user(netid, name, 'tutor', '1', session)

            # Admins
            admins_info = [
                ('dmbd', 'Dumbledore'),
                ('snp', 'Snape')
            ]
            for netid, name in admins_info:
                add_user(netid, name, 'admin', '1', session)
            
            session.commit()

            #-----------------------------------------------------------

            tutor1_info = database.Tutor(netid='hgranger', bio='MyBio 1')
            session.add(tutor1_info)
            tutor2_info = database.Tutor(netid='llvgd', bio='MyBio 2')
            session.add(tutor2_info)
            tutor3_info = database.Tutor(netid='pweasley', bio='MyBio 3')
            session.add(tutor3_info)
            session.commit()

            #-----------------------------------------------------------

            # DB for prototype. Generated with help from GPT.

            appointments_info = [
            {
                "time": datetime.datetime(2025, 3, 23, 9, 30),
                "tutor_netid": "hgranger",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 25, 14, 00),
                "tutor_netid": "llvgd",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 23, 11, 30),
                "tutor_netid": "hgranger",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 25, 11, 30),
                "tutor_netid": "hgranger",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 23, 14, 30),
                "tutor_netid": "pweasley",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 25, 17, 30),
                "tutor_netid": "llvgd",
                "booked": True,
                "student_netid": "nlongbottom",
                "comments": "my comments for appointment three",
                "coursenum": "1"
            },
            {
                "time": datetime.datetime(2025, 3, 27, 9, 30),
                "tutor_netid": "hgranger",
                "booked": True,
                "student_netid": "hpotter",
                "comments": "my comments for appointment three",
                "coursenum": "1"
            },
            {
                "time": datetime.datetime(2025, 3, 26, 15, 30),
                "tutor_netid": "hgranger",
                "booked": True,
                "student_netid": "ldraco",
                "comments": "my comments for appointment three",
                "coursenum": "1"
            },
            {
                "time": datetime.datetime(2025, 3, 25, 21, 30),
                "tutor_netid": "pweasley",
                "booked": True,
                "student_netid": "rweasley",
                "comments": "my comments for appointment",
                "coursenum": "1"
            },
            {
                "time": datetime.datetime(2025, 3, 24, 9, 00),
                "tutor_netid": "hgranger",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 24, 10, 30),
                "tutor_netid": "pweasley",
                "booked": True,
                "student_netid": "gweasley",
                "coursenum": "1"
            },
            {
                "time": datetime.datetime(2025, 3, 26, 14, 00),
                "tutor_netid": "llvgd",
                "booked": True,
                "student_netid": "cchang",
                "coursenum": "1"
            },
            {
                "time": datetime.datetime(2025, 3, 26, 16, 00),
                "tutor_netid": "pweasley",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 27, 10, 30),
                "tutor_netid": "hgranger",
                "booked": True,
                "student_netid": "ppatil",
                "coursenum": "1"
            },{
                "time": datetime.datetime(2025, 3, 24, 8, 00),
                "tutor_netid": "llvgd",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 24, 16, 00),
                "tutor_netid": "pweasley",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 26, 10, 00),
                "tutor_netid": "hgranger",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 27, 13, 00),
                "tutor_netid": "pweasley",
                "booked": False
            },{
                "time": datetime.datetime(2025, 3, 28, 9, 00),
                "tutor_netid": "hgranger",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 28, 17, 00),
                "tutor_netid": "llvgd",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 29, 15, 00),
                "tutor_netid": "pweasley",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 29, 12, 00),
                "tutor_netid": "llvgd",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 28, 11, 00),
                "tutor_netid": "hgranger",
                "booked": False
            },
            {
                "time": datetime.datetime(2025, 3, 26, 14, 00),
                "tutor_netid": "pweasley",
                "booked": False
            }
            ]
            for appt in appointments_info:
                add_appointment(session, **appt)

            session.commit()

        engine.dispose()

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
