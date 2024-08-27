#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Hita Gupta
#-----------------------------------------------------------------------

import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()

class User (Base):
    __tablename__ = 'users'
    netid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    user_type = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    coursenum = sqlalchemy.Column(sqlalchemy.String, primary_key=True)

class Tutor (Base):
    __tablename__ = 'tutors'
    netid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    bio = sqlalchemy.Column(sqlalchemy.String)

class Appointment (Base):
    __tablename__ = 'appointments'
    time = sqlalchemy.Column(sqlalchemy.DateTime, primary_key=True)
    booked = sqlalchemy.Column(sqlalchemy.Boolean)
    showed_up = sqlalchemy.Column(sqlalchemy.Boolean)
    tutor_netid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    student_netid = sqlalchemy.Column(sqlalchemy.String)
    comments = sqlalchemy.Column(sqlalchemy.String)
    coursenum = sqlalchemy.Column(sqlalchemy.String)
    location = sqlalchemy.Column(sqlalchemy.String)