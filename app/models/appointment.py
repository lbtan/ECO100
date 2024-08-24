#!/usr/bin/env python

#-----------------------------------------------------------------------
# appointment.py
# Authors: Hita Gupta 
#-----------------------------------------------------------------------

import datetime


class Appointment:

    def __init__(self, time, booked, tutor_netid, student_netid,
                 comments, coursenum, showed_up, location):
        self._time = time
        self._booked = booked
        self._tutor_netid = tutor_netid
        self._student_netid = student_netid
        self._comments = comments
        self._coursenum = coursenum
        self._showed_up = showed_up
        self._location = location

    def get_time(self):
        return self._time
    
    def get_booked(self):
        return self._booked

    def get_tutor_netid(self):
        return self._tutor_netid
    
    def get_student_netid(self):
        return self._student_netid
    
    def get_comments(self):
        return self._comments
    
    def get_coursenum(self):
        return self._coursenum
    
    def get_show(self):
        return self._showed_up

    def get_location(self):
        return self._location

    def to_tuple(self):
        return (self._time, self._booked, self._tutor_netid, 
                self._student_netid, self._comments, self._coursenum,
                self._showed_up, self._location)

#-----------------------------------------------------------------------

def _test():
    appt = Appointment(datetime.datetime(2024, 3, 14, 10, 30), 
                       True, 'tu123', 'st123', 'My comments', '40466')
    print(appt.get_time())
    print(appt.get_booked())
    print(appt.get_tutor_netid())
    print(appt.get_student_netid())
    print(appt.get_comments())
    print(appt.get_coursenum())
    print(appt.get_show())

if __name__ == '__main__':
    _test()
