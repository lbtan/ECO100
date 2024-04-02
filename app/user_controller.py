#-----------------------------------------------------------------------
# user_controller.py
# Authors: Libo Tan
# 
#
# Handles the logic of different views.
#-----------------------------------------------------------------------

import flask
import models.backend_tutor as db_tutor
import models.backend_student as db_student
import utils
from datetime import datetime
import models.db_modify as db_modify
import models.db_queries as db_queries
import models.backend_admin as backend_admin
import models.db_modify as db_modify

#----------------------------------------------------------------------#

app = flask.Flask(__name__, template_folder = 'templates',  static_folder='static')

#----------------------------------------------------------------------#

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

@app.route('/studentview')
def studentview():
    booked_appointments = db_student.get_cur_appoinments_student()
    # user id info
    #TODO fetch info from CAS
    user = ("Harry Potter", 'student', 'hpotter')
    # Parse db results
    cur_appointments = utils.appointments_by_student(booked_appointments, user[2])

    available_appointments = db_student.get_times_students()
    chronological_appointments = utils.available_appointments_by_time(available_appointments)

    html_code = flask.render_template('studentview.html', user=user, cur_appointments=cur_appointments,
                                      chronological_appointments=chronological_appointments, user_netid=user[2])
    response = flask.make_response(html_code)

    response.set_cookie('user_name', user[0])
    response.set_cookie('user_type', user[1])
    response.set_cookie('user_netid', user[2])
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
    html_code = flask.render_template('appointment_page.html', appointment=appt, user=user, tutor=tutor, student=student, date=date)
    response = flask.make_response(html_code)
    return response

@app.route('/appointment_confirm', methods=['POST'])
def appointment_confirm():
    date = flask.request.form.get('date')
    time = flask.request.form.get('time')
    tutor_netid = flask.request.form.get('tutor_netid')
    student_netid = flask.request.form.get('student_netid')
    comments = flask.request.form.get('comments')
    tutor_name = flask.request.form.get('tutor_name')
    
    datetime_str = f"{date} {time}"
    appt_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    db_modify.book_appointment(appt_time, tutor_netid, student_netid, comments, "1")
    
    user = get_user_from_cookies()
    html_code = flask.render_template('student_confirmation.html', user=user, tutor=tutor_name)
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

@app.route('/upload', methods=["POST"])
def upload():
    # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    uploaded_file = flask.request.files['file']

    # not working yet
    print(uploaded_file.filename)

    return flask.redirect(flask.url_for('adminview'))

@app.route('/add_appointment')
def add_appointment():
    tutor = flask.request.args.get('tutor_netid')
    date = flask.request.args.get('date')
    user = get_user_from_cookies()

    html_code = flask.render_template('add_appointment.html', user=user, tutor=tutor, date=date)
    response = flask.make_response(html_code)
    return response

@app.route('/add_appt_submit', methods=['POST'])
def add_appt_submit():
    date = flask.request.form['date']
    time = flask.request.form['time']
    tutor = flask.request.form['tutor']
    
    datetime_str = f"{date} {time}"
    appt_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
   
    db_modify.add_appointment(appt_time, tutor)

    return flask.redirect('/tutorview')

@app.route('/cancel_appointment')
def cancel_appointment():
    time = flask.request.args.get('time')
    tutor = flask.request.args.get('tutor_netid')
    user = get_user_from_cookies()
    
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    db_modify.cancel_appointment(time, tutor)

    return flask.redirect(flask.url_for(f"{user[1]}view"))