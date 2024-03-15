#!/usr/bin/env python

#-----------------------------------------------------------------------
# tutor.py
# Authors: Hita Gupta, ECO 100 Tutoring App Team 
#-----------------------------------------------------------------------

class Tutor:

    def __init__(self, netid, bio):
        self._netid = netid
        self._bio = bio

    def get_netid(self):
        return self._netid

    def get_bio(self):
        return self._bio

    def to_tuple(self):
        return (self._netid, self._bio)

#-----------------------------------------------------------------------

def _test():
    tutor = Tutor('tu123', 'This is my tutor bio.')
    print(tutor.get_netid())
    print(tutor.get_bio())
    print(tutor.to_tuple())

if __name__ == '__main__':
    _test()
