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
import random
from database import Appointment

dotenv.load_dotenv()
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
    

def add_appointment(session, time, tutor_netid, booked=False, student_netid=None, comments=None, coursenum=None, showed_up=None):
    """
    
    Functions that help with adding to database
    """
    
    appointment = database.Appointment(time=time, booked=booked, tutor_netid=tutor_netid,
                                       student_netid=student_netid, comments=comments, coursenum=coursenum, showed_up=showed_up)
    session.add(appointment)
    return

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)

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
            ('nlongbottom', 'Neville Longbottom'),
            ('fweasley', 'Fred Weasley'),
            ('gweasley2', 'George Weasley'),
            ('ppatil2', 'Parvati Patil'),
            ('cs-hd5234', 'Haichen Dong'),
            ('ldraco', 'Draco Malfoy'),
            ('gweasley', 'Ginny Weasley'),
            ('sfinnigan', 'Seamus Finnigan'),
        ]
        for netid, name in student_base_info:
            add_user(netid, name, 'student', '1',session)

        for netid in ['at6145', 'sm8765', 'hg7270', 'hd5234', 'anaikam', 'lgose', 'uchang', 'eag2', 'jc4557', 'elisem', 'jennyn', 'chaewonh', 'bo4', 'gw19', 'gloriawang', 'sls5']:
            user = database.User(netid=netid, name='', user_type='tester', coursenum="1")
            session.add(user)

        # Tutors
        tutors_info = [
            ('hgranger', 'Hermione Granger'),
            ('llvgd', 'Luna Lovegood'),
            ('pweasley', 'Percy Weasley'),
            ('habbott', 'Hannah Abbott'),
            ('cchang', 'Cho Chang'),
            ('ppatil', 'Padma Patil'),
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

        for i in range(len(tutors_info)):
            tutor_info = database.Tutor(netid=tutors_info[i][0], bio=f'MyBio {i+1}')
            session.add(tutor_info)
        session.commit()

        #-----------------------------------------------------------

        # DB for prototype. Generated with help from GPT.

        start_date = datetime.datetime(2024, 4, 25)
        end_date = datetime.datetime(2024, 5, 25)

        booked_appointments = {}  # Dictionary to track booked appointments for each student

        for _ in range(200):  # Generate 100 appointments
            time = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days),
                                                hours=random.randint(8, 21),
                                                minutes=random.choice([0, 30]))

            tutor_netid = random.choice([tutor[0] for tutor in tutors_info])
            booked = random.choice([True, False])
            showed_up = None

            existing_appointment = session.query(Appointment).filter_by(time=time, tutor_netid=tutor_netid).first()
            if existing_appointment:
                continue

            if booked:
                week_number = time.isocalendar()[1]
                appointments_this_week = booked_appointments.get(week_number, {}).keys()

                if len(appointments_this_week) == len(student_base_info):
                    continue  # Skip this iteration if all students already have appointments this week

                available_students = [student for student in student_base_info if student[0] not in appointments_this_week]
                student_netid = random.choice(available_students)[0]
            else:
                student_netid = None

            comments = "my comments for appointment" if booked else None
            coursenum = '1'

            # Update booked_appointments dictionary
            if booked:
                week_number = time.isocalendar()[1]
                if week_number not in booked_appointments:
                    booked_appointments[week_number] = {}
                booked_appointments[week_number][student_netid] = time

            add_appointment(session, time, tutor_netid, booked, student_netid, comments, coursenum, showed_up)

        session.commit()

    engine.dispose()

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
