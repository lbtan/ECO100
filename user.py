#!/usr/bin/env python

#-----------------------------------------------------------------------
# user.py
# Authors: Hita Gupta, ECO 100 Tutoring App Team 
#-----------------------------------------------------------------------

class User:

    def __init__(self, netid, name, user_type, coursenum):
        self._netid = netid
        self._name = name
        self._user_type = user_type
        self._coursenum = coursenum

    def get_netid(self):
        return self._netid

    def get_name(self):
        return self._name

    def get_user_type(self):
        return self._user_type
    
    def get_coursenum(self):
        return self._coursenum

    def to_tuple(self):
        return (self._netid, self._name, self._user_type, 
                self._coursenum)

#-----------------------------------------------------------------------

def _test():
    user = User('st123', 'My Name', 'Student', '40466')
    print(user.get_netid())
    print(user.get_name())
    print(user.get_user_type())
    print(user.get_coursenum())
    print(user.to_tuple())

if __name__ == '__main__':
    _test()
