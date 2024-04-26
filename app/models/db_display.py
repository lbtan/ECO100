#!/usr/bin/env python

#-----------------------------------------------------------------------
# db_display.py
# Author: Hita Gupta
#-----------------------------------------------------------------------

# for debugging

import os
import sys
import sqlalchemy
import sqlalchemy.orm
import dotenv
import database

DATABASE_URL= "postgres://eco100_tutoring_user:hmva48rjXFOw1y6DEoUquq6EpnfT3sKX@dpg-coc3d48l5elc739mcnag-a.ohio-postgres.render.com/eco100_tutoring"
_DATABASE_URL = DATABASE_URL
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)
        sys.exit(1)

    try:
        engine = sqlalchemy.create_engine(_DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:

            print('-------------------------------------------')
            print('users')
            print('-------------------------------------------')
            query = session.query(database.User)
            table = query.all()
            for row in table:
                print(row.netid, row.name, row.user_type, row.coursenum)

            print('-------------------------------------------')
            print('tutors')
            print('-------------------------------------------')
            query = session.query(database.Tutor)
            table = query.all()
            for row in table:
                print(row.netid, row.bio)

            print('-------------------------------------------')
            print('appointments')
            print('-------------------------------------------')
            query = session.query(database.Appointment)
            table = query.all()
            for row in table:
                print(row.time, row.booked, row.tutor_netid, 
                      row.student_netid, row.comments, row.coursenum, row.showed_up)

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
