#!/usr/bin/env python

#-----------------------------------------------------------------------
# db_create.py
# Author: Hita Gupta, ECO 100 Tutoring App Team
#-----------------------------------------------------------------------

import os
import sys
import sqlalchemy
import sqlalchemy.orm
import dotenv
import database
import datetime

dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)
        sys.exit(1)

    try:
        engine = sqlalchemy.create_engine(_DATABASE_URL)

        database.Base.metadata.drop_all(engine)
        database.Base.metadata.create_all(engine)

        with sqlalchemy.orm.Session(engine) as session:

            #-----------------------------------------------------------
            
            student1 = database.User(netid='st111',name='Student One',
                                     user_type='student',coursenum='1')
            session.add(student1)
            student2 = database.User(netid='st222',name='Student Two',
                                     user_type='student',coursenum='1')
            session.add(student2)

            tutor1 = database.User(netid='tu111',name='Tutor One',
                                     user_type='tutor',coursenum='1')
            session.add(tutor1)
            tutor2 = database.User(netid='tu222',name='Tutor Two',
                                     user_type='tutor',coursenum='1')
            session.add(tutor2)

            admin1 = database.User(netid='ad111',name='Admin CourseOne',
                                     user_type='admin',coursenum='1')
            session.add(admin1)
            admin2 = database.User(netid='ad222',name='Admin CourseTwo',
                                     user_type='admin',coursenum='2')
            session.add(admin2)

            session.commit()

            #-----------------------------------------------------------

            tutor1_info = database.Tutor(netid='tu111', bio='MyBio 1')
            session.add(tutor1_info)
            tutor2_info = database.Tutor(netid='tu222', bio='MyBio 2')
            session.add(tutor2_info)
            tutor3_info = database.Tutor(netid='tu333', bio='MyBio 3')
            session.add(tutor3_info)
            session.commit()

            #-----------------------------------------------------------

            appointment1 = database.Appointment(time=datetime.datetime(
                2024, 3, 14, 9, 30), booked=False, tutor_netid='tu111')
            session.add(appointment1)
            
            appointment2 = database.Appointment(time=datetime.datetime(
                2024, 3, 16, 9, 30), booked=False, tutor_netid='tu222')
            session.add(appointment2)

            appointment3 = database.Appointment(time=datetime.datetime(
                2024, 3, 18, 9, 30), booked=True, tutor_netid='tu111',
                student_netid='st222', comments='my comments for ' +
                'appointment three', coursenum='1')
            session.add(appointment3)

            appointment4 = database.Appointment(time=datetime.datetime(
                2024, 3, 16, 11, 30), booked=False, tutor_netid='tu333')
            session.add(appointment4)

            session.commit()

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
