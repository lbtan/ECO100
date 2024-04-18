#-----------------------------------------------------------------------
# user_controller.py
# Authors: Libo Tan, Sofia Marina
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
import auth
import dotenv, os
import ssl

#  https://stackoverflow.com/questions/44649449/brew-installation-of-python-3-6-1-ssl-certificate-verify-failed-certificate/44649450#44649450 
ssl._create_default_https_context = ssl._create_stdlib_context

#----------------------------------------------------------------------#

# for testing purposes
testing_ids = db_queries.get_testing_ids()

app = flask.Flask(__name__, template_folder = 'templates',  static_folder='static')

# CAS authentication stuff
dotenv.load_dotenv()
os.environ['APP_SECRET_KEY']
app.secret_key = os.environ['APP_SECRET_KEY']


#-----------------------------------------------------------------------

def authorize(username):
    if username not in testing_ids:
        html = flask.render_template('error_handling/unauth.html')
        response = flask.make_response(html)
        flask.abort(response)

#----------------------------------------------------------------------#

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

@app.route('/user_type', methods = ['GET'])
def user_type():
    username = auth.authenticate()
    print(username)
    authorize(username)
    html_code = flask.render_template('user_type.html')  
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

# Routes for authentication.

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

#-----------------------------------------------------------------------

# Student view

@app.route('/studentview')
def studentview():
    username = auth.authenticate()
    authorize(username)
    booked_appointments = db_student.get_cur_appoinments_student()
    # user id info
    user = ("Harry Potter", 'student', "hpotter")
    # Parse db results
    cur_appointments = utils.appointments_by_student(booked_appointments, user[2])
    
    booked_appointments = db_student.get_cur_appoinments_student()
    available_appointments = db_student.get_times_students()
    chronological_appointments = utils.available_appointments_by_time(available_appointments, booked_appointments)

    html_code = flask.render_template('student/studentview.html', user=user, cur_appointments=cur_appointments,
                                      can_book = len(cur_appointments) == 0,
                                      appointments_by_date=chronological_appointments)
    response = flask.make_response(html_code)

    response.set_cookie('user_name', user[0])
    response.set_cookie('user_type', user[1])
    response.set_cookie('user_netid', user[2])
    return response


#-----------------------------------------------------------------------

# Tutor view 

@app.route('/tutorview')
def tutorview():
    username = auth.authenticate()
    authorize(username)
    appointments = db_tutor.get_times_tutors()
    # user id info
    #TODO fetch info from CAS
    user = ("Hermione Granger", 'tutor', "hgranger")
    # Parse db results
    apt_tutor = utils.appointments_by_tutor(appointments, user[2])
    apt_times = utils.appointments_by_time(appointments)
    html_code = flask.render_template('tutor/tutorview.html', appointments_by_date=apt_times, user=user, apt_tutor=apt_tutor)
    response = flask.make_response(html_code)

    response.set_cookie('user_name', user[0])
    response.set_cookie('user_type', user[1])
    response.set_cookie('user_netid', user[2])
    return response

@app.route('/tutor_bio_edit')
def tutor_bio_edit():
    tutor_netid = flask.request.args.get('tutor_netid')
    bio = db_queries.get_tutor_bio(tutor_netid)
    html_code = flask.render_template('tutor/tutor_bio_edit.html', tutor_netid=tutor_netid, bio=bio)
    response = flask.make_response(html_code)
    return response

@app.route('/tutor_bio_edit_submit', methods=['POST'])
def tutor_bio_edit_submit():
    tutor_netid = flask.request.form.get('tutor_netid')
    bio = flask.request.form.get('bio')
    db_modify.update_tutor_bio(tutor_netid, bio)
    return flask.redirect(flask.url_for('tutorview'))

#-----------------------------------------------------------------------

# Admin view

@app.route('/adminview')
def adminview():
    username = auth.authenticate()
    authorize(username)
    try:
        upload_message = flask.request.args.get('upload_message')
    except:
        pass

    appointments = db_tutor.get_times_tutors()
    apt_times = utils.appointments_by_time(appointments)
    user = (username, 'admin', username)

    html_code = flask.render_template('admin/adminview.html', user=user, appointments_by_date=apt_times, upload_message=upload_message)
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


#-----------------------------------------------------------------------

@app.route('/appointment_popup')
def appointment_popup():
    username = auth.authenticate()
    authorize(username)
    tutor = flask.request.args.get('tutor_netid')
    date = flask.request.args.get('date')
    time = flask.request.args.get('time')

    user = get_user_from_cookies()
    print(user)

    datetime_str = f"{date} {time}"
    appt_time = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
    appts = db_queries.get_appointments({"tutor_netid": tutor, "exact_time": appt_time})
    if appts[0] == False:
        html_code = flask.render_template('error_handling/db_error.html')
        response = flask.make_response(html_code)
        return response
    appt = appts[0] # should only match one appointment

    tutor = db_queries.get_user_info({"netid": appt.get_tutor_netid(), "user_type": "tutor"})[0]
    if tutor == False:
        html_code = flask.render_template('error_handling/db_error.html')
        response = flask.make_response(html_code)
        return response

    if appt.get_student_netid():
        student = db_queries.get_user_info({"netid": appt.get_student_netid(), "user_type": "student"})[0]
        if student == False:
            html_code = flask.render_template('error_handling/db_error.html')
            response = flask.make_response(html_code)
            return response
    else:
        student = None

    # https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event
    html_code = flask.render_template('appointment_popup.html', appointment=appt, user=user, tutor=tutor, student=student, date=date)
    response = flask.make_response(html_code)
    return response

@app.route('/appointment_confirm', methods=['POST'])
def appointment_confirm():
    username = auth.authenticate()
    authorize(username)
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
    html_code = flask.render_template('student/student_confirmation.html', user=user, tutor=tutor_name)
    response = flask.make_response(html_code)
    return response

@app.route('/weekly_summary')
def weekly_summary():
    username = auth.authenticate()
    authorize(username)
    user = get_user_from_cookies()

    # for now everything is under coursenum 1, and all data is under March 2025
    summary = backend_admin.weekly_summary("1", datetime(2025, 3, 30)) 
    if summary == False:
        html_code = flask.render_template('error_handling/db_error.html')
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('admin/weekly_summary.html', summary=summary, user=user)
    response = flask.make_response(html_code)
    return response

@app.route('/tutor_overview')
def tutor_overview():
    username = auth.authenticate()
    authorize(username)
    user = get_user_from_cookies()
    users = db_queries.get_user_info({"user_type": "tutor", "coursenum": "1"})
    if users[0] == False:
        html_code = flask.render_template('error_handling/db_error.html')
        response = flask.make_response(html_code)
        return response
    
    names_bios = {}
    for curr_user in users:
        name = curr_user.get_name()
        netid = curr_user.get_netid()
        bio = db_queries.get_tutor_bio(netid)
        if bio[0] == False:
            html_code = flask.render_template('error_handling/db_error.html')
            response = flask.make_response(html_code)
            return response
        names_bios[name] = bio

    html_code = flask.render_template('admin/tutor_overview.html', names_bios=names_bios, user=user)
    response = flask.make_response(html_code)
    return response

@app.route('/upload', methods=["POST"])
def upload():
    username = auth.authenticate()
    authorize(username)
    # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    user_type = flask.request.form['user_type']
    uploaded_file = flask.request.files['users_file']
    filename = uploaded_file.filename
    if filename == '' or os.path.splitext(filename)[-1] != 'csv':
        message = 'Please upload a valid .csv file.'
    else:
        message = backend_admin.import_users(uploaded_file, user_type, "1")
    return flask.redirect(flask.url_for('adminview', upload_message=message))

@app.route('/add_appointment')
def add_appointment():
    username = auth.authenticate()
    authorize(username)
    tutor = flask.request.args.get('tutor_netid')
    date = flask.request.args.get('date')
    user = get_user_from_cookies()

    html_code = flask.render_template('tutor/add_appointment.html', user=user, tutor=tutor, date=date)
    response = flask.make_response(html_code)
    return response

@app.route('/add_appt_submit', methods=['POST'])
def add_appt_submit():
    username = auth.authenticate()
    authorize(username)
    date = flask.request.form['date']
    time = flask.request.form['time']
    tutor = flask.request.form['tutor']
    
    datetime_str = f"{date} {time}"
    appt_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
   
    db_modify.add_appointment(appt_time, tutor)

    return flask.redirect('/tutorview')

@app.route('/cancel_appointment')
def cancel_appointment():
    username = auth.authenticate()
    authorize(username)
    time = flask.request.args.get('time')
    tutor = flask.request.args.get('tutor_netid')
    user = get_user_from_cookies()
    
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    db_modify.cancel_appointment(time, tutor)

    return flask.redirect(flask.url_for(f"{user[1]}view"))

@app.route('/edit_appointment', methods=['POST'])
def edit_appointment():
    username = auth.authenticate()
    authorize(username)
    date = flask.request.form['date']
    prev_time = flask.request.form['prev-time'][:-3] # remove seconds
    tutor = flask.request.form['tutor_netid']
    new_time = flask.request.form['new-time'][:-3] # remove seconds
    
    datetime_str = f"{date} {new_time}"
    new_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

    datetime_str = f"{date} {prev_time}"
    prev_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
   
    db_modify.modify_appointment_time(prev_time, new_time, tutor)

    return flask.redirect('/tutorview')
