#-----------------------------------------------------------------------
# user_controller.py
# Authors: Libo Tan
# 
#
# Handles the logic of different views.
#-----------------------------------------------------------------------

import flask
import models.backend_tutor as db_tutor
import utils
from datetime import datetime
import models.db_queries as db_queries
import models.backend_admin as backend_admin

#----------------------------------------------------------------------#

app = flask.Flask(__name__, template_folder = 'templates',  static_url_path='/static')

#----------------------------------------------------------------------#

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

@app.route('/studentview')
def studentview():
    html_code = flask.render_template('studentview.html')
    response = flask.make_response(html_code)
    return response

@app.route('/tutorview')
def tutorview():
    appointments = db_tutor.get_times_tutors()
    # user id info
    #TODO fetch info from CAS
    user = ("Hermione Granger", 'tutor', 'hgranger')
    # Parse db results
    apt_tutor = utils.appointments_by_tutor(appointments, user[2])
    apt_times = utils.appointments_by_time(appointments)
    html_code = flask.render_template('tutorview.html', appointments_by_date=apt_times, user=user, apt_tutor=apt_tutor)
    response = flask.make_response(html_code)

    response.set_cookie('user_name', user[0])
    response.set_cookie('user_type', user[1])
    response.set_cookie('user_netid', user[2])
    return response

@app.route('/adminview')
def adminview():
    appointments = db_tutor.get_times_tutors()
    apt_times = utils.appointments_by_time(appointments)
    user  = ('Dumbledore', 'admin', 'dmbd')

    html_code = flask.render_template('adminview.html', user=user, appointments_by_date=apt_times)
    response = flask.make_response(html_code)

    response.set_cookie('user_name', user[0])
    response.set_cookie('user_type', user[1])
    response.set_cookie('user_netid', user[2])
    return response

def get_user_from_cookies():
    name = flask.request.cookies.get('user_name')
    type = flask.request.cookies.get('user_type')
    netid = flask.request.cookies.get('user_netid')
    user = (name, type, netid)
    return user

@app.route('/appointment_page')
def appointment_page():
    tutor = flask.request.args.get('tutor_netid')
    date = flask.request.args.get('date')
    time = flask.request.args.get('time')

    user = get_user_from_cookies()

    datetime_str = f"{date} {time}"
    appt_time = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
    appts = db_queries.get_appointments({"tutor_netid": tutor, "exact_time": appt_time})
    appt = appts[0] # should only match one appointment

    tutor = db_queries.get_user_info({"netid": appt.get_tutor_netid(), "user_type": "tutor"})[0]

    if appt.get_student_netid():
        student = db_queries.get_user_info({"netid": appt.get_student_netid(), "user_type": "student"})[0]
    else:
        student = None

    # https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event
    html_code = flask.render_template('appointment_page.html', appointment=appt, user=user, tutor=tutor, student=student)
    response = flask.make_response(html_code)
    return response

@app.route('/weekly_summary')
def weekly_summary():
    user = get_user_from_cookies()

    # for now everything is under coursenum 1, and all data is under March 2025
    summary = backend_admin.weekly_summary("1", datetime(2025, 3, 30)) 

    html_code = flask.render_template('weekly_summary.html', summary=summary, user=user)
    response = flask.make_response(html_code)
    return response

@app.route('/tutor_overview')
def tutor_overview():
    user = get_user_from_cookies()
    users = db_queries.get_user_info({"user_type": "tutor", "coursenum": "1"})
    
    names_bios = {user.get_name(): db_queries.get_tutor_bio(user.get_netid()) for user in users}

    html_code = flask.render_template('tutor_overview.html', names_bios=names_bios, user=user)
    response = flask.make_response(html_code)
    return response