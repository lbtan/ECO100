#-----------------------------------------------------------------------
# user_controller.py
# Authors: Libo Tan, Sofia Marina, Hita Gupta, Anaika Mehra
# 
#
# Handles the logic of different views.
#-----------------------------------------------------------------------

import flask
from flask_mail import Mail
import models.backend_tutor as db_tutor
import models.backend_student as db_student
import utils
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import models.db_modify as db_modify
import models.db_queries as db_queries
import models.backend_admin as backend_admin
import models.db_modify as db_modify
import auth
import dotenv, os
import ssl
import models.send_email as send_email
from models.date import today

#  https://stackoverflow.com/questions/44649449/brew-installation-of-python-3-6-1-ssl-certificate-verify-failed-certificate/44649450#44649450 
ssl._create_default_https_context = ssl._create_stdlib_context

# Load environment variables
dotenv.load_dotenv()

#----------------------------------------------------------------------#

# for testing purposes
testing_ids = db_queries.get_testing_ids()
student_ids = utils.get_student_ids()
tutor_ids = utils.get_tutor_ids()
admin_ids = utils.get_admin_ids()
netids_to_names = utils.get_names()
# Role to ID mapping
id_map = {
    'testing': testing_ids,
    'student': student_ids,
    'tutor': tutor_ids,
    'admin': admin_ids
}

app = flask.Flask(__name__, template_folder = 'templates',  static_folder='static')

SEND_MAIL = False

# Mail
if SEND_MAIL:
    print("Email notification activated.")
    mail_username = os.environ['MAIL_USERNAME']
    mail_password = os.environ['MAIL_PASSWORD']

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = mail_username
    app.config['MAIL_PASSWORD'] = mail_password
    mail = Mail(app)
    mail_sender = send_email.MailSender(mail, mail_username)

#-----------------------------------------------------------------------

# CAS authentication stuff
os.environ['APP_SECRET_KEY']
app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------

def failed_authorize():
    """
    Failed authen
    """
    html = flask.render_template('error_handling/unauth.html')
    response = flask.make_response(html)
    flask.abort(response)


#-----------------------------------------------------------------------#

def authorize(username, types):
    """
    Check if the user has access to each page.
    """
    if isinstance(types, str):
        types = [types]

    # Special access for "testing" type
    if username in testing_ids:
        print(f"Authorization granted: {username} as tester.")
        return True
    
    for type in types:
        # Check if the type is valid
        if type not in id_map:
            print(f"Authorization error: Unknown type '{type}'.")
            failed_authorize()

        # Retrieve the correct ID list based on the type
        role_ids = id_map[type]
        if username in role_ids:
            print(f"Authorization successful for {username}.")
            return True
    # print(admin_ids)
    print(f"Authorization failed for user '{username}'. Not found in ids for type(s): {', '.join(types)}.")
    failed_authorize()

#----------------------------------------------------------------------#

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

@app.route('/user_type', methods = ['GET'])
def user_type():
    """
    Direct user to respective view of different pages.
    """
    username = auth.authenticate()
    # username = 'hpotter'
    if username in testing_ids:
        print("Authorized ", username, " as tester.")
        html_code = flask.render_template('user_type.html')  
    elif username in student_ids:
        print("Authorized ", username, " as student.")
        return flask.redirect(flask.url_for('studentview'))
    elif username in tutor_ids:
        print("Authorized ", username, " as tutor.")
        return flask.redirect(flask.url_for('tutorview'))
    elif username in admin_ids:
        print("Authorized ", username, " as admin")
        return flask.redirect(flask.url_for('adminview'))
    else:
        failed_authorize()
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

# https://flask.palletsprojects.com/en/3.0.x/errorhandling/
@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('error_handling/404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return flask.render_template('error_handling/500.html'), 500

#-----------------------------------------------------------------------

@app.route('/get_student_ids')
def get_student_ids():
    return flask.render_template('netid_modal.html', netids=student_ids, modal_id="studentIdModal", user_type='student')


@app.route('/get_tutor_ids')
def get_tutor_ids():
    return flask.render_template('netid_modal.html', netids=tutor_ids, modal_id="tutorIdModal", user_type='tutor')


@app.route('/get_admin_ids')
def get_admin_ids():
    return flask.render_template('netid_modal.html', netids=admin_ids, modal_id="adminIdModal", user_type='admin')


@app.route('/process_netid_selection', methods=['POST'])
def process_netid_selection():
    selected_netid = flask.request.form['selectedNetID']
    user_type = flask.request.form['userType'] 
    print("Selected NetID:", selected_netid, "User Type:", user_type)

    if user_type == 'student':
        return flask.redirect(flask.url_for('studentview', netid=selected_netid))
    elif user_type == 'tutor':
        return flask.redirect(flask.url_for('tutorview', netid=selected_netid))
    elif user_type == 'admin':
        return flask.redirect(flask.url_for('adminview', netid=selected_netid))
    else:
        flask.flash("Invalid user type provided.")
        html_code = flask.render_template('error_handling/db_error.html')
        return flask.make_response(html_code)


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
@app.route('/studentview', defaults={'netid': None})
@app.route('/studentview/<netid>')
def studentview(netid):

    username = auth.authenticate()
    # security testing  
    # username = 'hpotter'

    # handle case for test user 
    # Check if username is a tester
    if username in testing_ids:
        if netid is None:
            # Direct to a specific page for testers when no netid is provided
            html_code = flask.render_template('user_type.html')
            return flask.make_response(html_code)
        elif netid == username or netid in testing_ids:
            print(f"Authorization failed for user '{username}'. Page does not exist.")
            html = flask.render_template('error_handling/404.html')
            response = flask.make_response(html)
            flask.abort(response)
        elif netid != username:
            # If netid is different from username and user is a tester, check netid is a student
            authorize(netid, 'student')


    # Normal users trying to access their own information or when netid is None
    if netid is None or netid == username:
        authorize(username, 'student')
    
    # deny access to other pages
    if netid is not None and netid != username:
        authorize(username, 'testing')
    
    if netid is None:
        netid = username
    # only allow free netid access for testers
    print("netid: ", netid, "username: ", username)

    booked_appointments = db_student.get_cur_appoinments_student()
    # user id info
    user = (netids_to_names[netid], 'student', netid)
    # Parse db results
    cur_appointments = utils.appointments_by_student(booked_appointments, user[2])

    available_appointments = db_student.get_times_students()
    chronological_appointments = utils.available_appointments_by_time(available_appointments, booked_appointments)
    weekly_appointments = utils.group_by_week(chronological_appointments)

    can_book = utils.get_can_book(cur_appointments, weekly_appointments)

    unique_names = set()

    # Iterate through the outer dictionary to access each inner dictionary
    for date, names_dict in chronological_appointments.items():
        # Add each key (name) from the inner dictionary to the set (automatically handles uniqueness)
        unique_names.update(names_dict.keys())

    names_bios = {}
    for curr_user in unique_names:
        bio = db_queries.get_tutor_bio(curr_user)
        if len(bio) > 0 and bio[0] == False:
            html_code = flask.render_template('error_handling/db_error.html')
            response = flask.make_response(html_code)
            return response
        names_bios[curr_user] = bio

    html_code = flask.render_template('student/studentview.html', user=user, cur_appointments=cur_appointments,
                                      can_book = can_book,
                                      appointments_by_date=chronological_appointments,
                                      names_bios = names_bios,
                                      names=netids_to_names, weekly_appointments=weekly_appointments)
    response = flask.make_response(html_code)

    response.set_cookie('user_name', user[0])
    response.set_cookie('user_type', user[1])
    response.set_cookie('user_netid', user[2])
    return response


#-----------------------------------------------------------------------

# Tutor view 
@app.route('/tutorview', defaults={'netid': None})
@app.route('/tutorview/<netid>')
def tutorview(netid):
    
    username = auth.authenticate()
    #username = 'hpotter'
    # handle case for test user 
    # Check if username is a tester
    if username in testing_ids:
        if netid is None:
            # Direct to a specific page for testers when no netid is provided
            html_code = flask.render_template('user_type.html')
            return flask.make_response(html_code)
        elif netid == username or netid in testing_ids:
            print(f"Authorization failed for user '{username}'. Page does not exist.")
            html = flask.render_template('error_handling/404.html')
            response = flask.make_response(html)
            flask.abort(response)
        elif netid != username:
            # If netid is different from username and user is a tester, check netid is a student
            authorize(netid, 'tutor')
        

    # Normal users trying to access their own information or when netid is None
    if netid is None or netid == username:
        authorize(username, 'tutor')
    
    # deny access to other pages
    if netid is not None and netid != username:
        authorize(username, 'testing')
    
    if netid is None:
        netid = username
    # only allow free netid access for testers
    print("netid: ", netid, "username: ", username)
    
    appointments = db_tutor.get_times_tutors()

    # user id info
    user = (netids_to_names[netid], 'tutor', netid)
    # Parse db results
    apt_tutor = utils.appointments_by_tutor(appointments, user[2])
    apt_times = utils.appointments_by_time(appointments, user[2])
    weekly_appointments = utils.group_by_week(apt_times)

    prev_appointments = db_tutor.get_prev_times(user[2])
    no_show_appointments = []
    for row in prev_appointments:
        if row[2] and row[-1] is None:
            no_show_appointments.append(row)
    
    # user id info
    user = (netids_to_names[netid], 'tutor', netid)
    # Parse db results
    apt_tutor = utils.appointments_by_tutor(appointments, user[2])
    apt_times = utils.appointments_by_time(appointments, user[2])
    weekly_appointments = utils.group_by_week(apt_times)
    html_code = flask.render_template('tutor/tutorview.html', weekly_appointments=weekly_appointments, user=user, apt_tutor=apt_tutor, names=netids_to_names, no_show_appointments = no_show_appointments)
    response = flask.make_response(html_code)

    response.set_cookie('user_name', user[0])
    response.set_cookie('user_type', user[1])
    response.set_cookie('user_netid', user[2])
    return response

@app.route('/tutor_bio_edit')
def tutor_bio_edit():
    username = auth.authenticate()
    authorize(username, 'tutor')

    tutor_netid = flask.request.args.get('tutor_netid')
    bio = db_queries.get_tutor_bio(tutor_netid)
    html_code = flask.render_template('tutor/tutor_bio_edit.html', tutor_netid=tutor_netid, bio=bio)
    response = flask.make_response(html_code)
    return response

@app.route('/tutor_bio_edit_submit', methods=['POST'])
def tutor_bio_edit_submit():
    username = auth.authenticate()
    authorize(username, 'tutor')

    tutor_netid = flask.request.form.get('tutor_netid')
    bio = flask.request.form.get('bio')
    db_modify.update_tutor_bio(tutor_netid, bio)
    user = get_user_from_cookies()
    return flask.redirect(flask.url_for('tutorview', netid=user[2]))

@app.route('/confirm_copy_times')
def confirm_copy_times():
    username = auth.authenticate()
    authorize(username, 'tutor')

    min_date = flask.request.args.get('min_date')
    max_date = flask.request.args.get('max_date')

    min_date = datetime.strptime(min_date, '%Y-%m-%d')
    max_date = datetime.strptime(max_date, '%Y-%m-%d')    

    html_code = flask.render_template('tutor/confirm_copy_times.html', min_date=min_date, max_date=max_date)
    response = flask.make_response(html_code)
    return response

@app.route('/copy_prev_week')
def copy_prev_week():
    username = auth.authenticate()
    authorize(username, 'tutor')

    min_date = flask.request.args.get('min_date')
    max_date = flask.request.args.get('max_date')
    
    min_date = datetime.strptime(min_date, '%Y-%m-%d')
    max_date = datetime.strptime(max_date, '%Y-%m-%d')

    user = get_user_from_cookies()
    db_tutor.copy_prev_week_times(min_date, max_date, user[2])
    return flask.redirect(flask.url_for('tutorview', netid=user[2]))

@app.route('/no_show_update')
def no_show_update():
    username = auth.authenticate()
    authorize(username, 'tutor')

    time = flask.request.args.get('time')
    tutor = flask.request.args.get('tutor_netid')
    showed_up = flask.request.args.get('value')
    showed_up = True if showed_up == "True" else False
    user = get_user_from_cookies()
    
    time = datetime.strptime(time, '%Y-%m-%d %I:%M %p')

    db_modify.update_showed_up(tutor, time, showed_up)

    return flask.redirect(flask.url_for('tutorview', netid=user[2]))

#-----------------------------------------------------------------------

# Admin view
@app.route('/adminview', defaults={'netid': None})
@app.route('/adminview/<netid>')
def adminview(netid):
    username = auth.authenticate()
    # username = 'hpotter'
    # handle case for test user 
    # Check if username is a tester
    if username in testing_ids:
        if netid is None:
            # Direct to a specific page for testers when no netid is provided
            html_code = flask.render_template('user_type.html')
            return flask.make_response(html_code)
        elif netid == username or netid in testing_ids:
            print(f"Authorization failed for user '{username}'. Page does not exist.")
            html = flask.render_template('error_handling/404.html')
            response = flask.make_response(html)
            flask.abort(response)
        elif netid != username:
            # If netid is different from username and user is a tester, check netid is a student
            authorize(netid, 'admin')

    # Normal users trying to access their own information or when netid is None
    if netid is None or netid == username:
        authorize(username, 'admin')
    
    # deny access to other pages
    if netid is not None and netid != username:
        authorize(username, 'testing')
    
    if netid is None:
        netid = username
    # only allow free netid access for testers
    print("netid: ", netid, "username: ", username)
    
    appointments = db_tutor.get_times_tutors()
    apt_times = utils.appointments_by_time(appointments)
    weekly_appointments = utils.group_by_week(apt_times)
    
    user = (netids_to_names[netid], 'admin', netid)

    html_code = flask.render_template('admin/adminview.html', user=user, weekly_appointments=weekly_appointments, names=netids_to_names)
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
    tutor = flask.request.args.get('tutor_netid')
    date = flask.request.args.get('date')
    time = flask.request.args.get('time')

    user = get_user_from_cookies()

    # Find the appointment
    datetime_str = f"{date} {time}"
    appt_time = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
    appts = db_queries.get_appointments({"tutor_netid": tutor, "exact_time": appt_time})
    if len(appts) > 0 and appts[0] == False:
        html_code = flask.render_template('appointment_popup.html', error='A database error has occured. Please contact the system administrator.', title='Error')
        response = flask.make_response(html_code)
        return response
    appt = appts[0] # should only match one appointment

    # If the user is a tutor and this is not their appointment, they cannot access its details
    if user[1] == "tutor" and user[2] != appt.get_tutor_netid():
        html_code = flask.render_template('appointment_popup.html', error='Sorry, you are unauthorized to view this page.', title='Unauthorized')
        response = flask.make_response(html_code)
        return response
    
    # If the user is a student and they already have an appointment booked for this week, they cannot access this one
    if user[1] == "student":
        booked_appointments = db_student.get_cur_appoinments_student()
        cur_appointments = utils.appointments_by_student(booked_appointments, user[2])
        weeks = set([appt[0].isocalendar()[:2] for appt in cur_appointments])
        if appt.get_time().isocalendar()[:2] in weeks and appt.get_student_netid() != user[2]:
            html_code = flask.render_template('appointment_popup.html', error='Sorry, you are unauthorized to view this page.', title='Unauthorized')
            response = flask.make_response(html_code)
            return response

    # Get the details of the tutor for this appointment
    tutor = db_queries.get_user_info({"netid": appt.get_tutor_netid(), "user_type": "tutor"})[0]
    if tutor == False:
        html_code = flask.render_template('appointment_popup.html', error='A database error has occured. Please contact the system administrator.', title='Error')
        response = flask.make_response(html_code)
        return response

    # If the appointment is booked, get the details of the student for this appointment
    if appt.get_student_netid():
        student = db_queries.get_user_info({"netid": appt.get_student_netid(), "user_type": "student"})[0]
        if student == False:
            html_code = flask.render_template('appointment_popup.html', error='A database error has occured. Please contact the system administrator.', title='Error')
            response = flask.make_response(html_code)
            return response
    else:
        student = None

    if appt.get_booked() or user[1] == "admin":
        title = 'Appointment Details'
    elif user[1] == "student":
        title = 'Book Appointment'
    else:
        title = 'Edit Appointment'

    # https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event
    html_code = flask.render_template('appointment_popup.html', appointment=appt, user=user, tutor=tutor, student=student, date=date, title=title)
    response = flask.make_response(html_code)
    return response

@app.route('/appointment_confirm', methods=['POST'])
def appointment_confirm():
    username = auth.authenticate()
    authorize(username, 'student')
    date = flask.request.form.get('date')
    time = flask.request.form.get('time')
    tutor_netid = flask.request.form.get('tutor_netid')
    student_netid = flask.request.form.get('student_netid')
    comments = flask.request.form.get('comments')
    tutor_name = flask.request.form.get('tutor_name')
    
    datetime_str = f"{date} {time}"
    appt_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

    status, _ = db_modify.book_appointment(appt_time, tutor_netid, student_netid, comments, "1")
    if not status:
        html_code = flask.render_template('error_handling/error.html', error="Sorry, this appointment is already booked. Please choose another time.")
        response = flask.make_response(html_code)
        return response

    if SEND_MAIL:
        tutor = db_queries.get_user_info({"netid": tutor_netid, "user_type": "tutor"})[0]
        student = db_queries.get_user_info({"netid": student_netid, "user_type": "student"})[0]
        mail_sender.book_appointment(appt_time, student, tutor, comments)
    
    user = get_user_from_cookies()
    html_code = flask.render_template('student/student_confirmation.html', user=user, tutor=tutor_name)
    response = flask.make_response(html_code)
    return response

@app.route('/weekly_summary')
def weekly_summary():
    username = auth.authenticate()
    authorize(username, 'admin')
    user = get_user_from_cookies()

    # for now everything is under coursenum 1
    summary, dates = backend_admin.weekly_summary("1") 
    if summary == False:
        html_code = flask.render_template('error_handling/db_error.html')
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('admin/weekly_summary.html', summary=summary, user=user, dates=dates, names=netids_to_names)
    response = flask.make_response(html_code)
    return response

@app.route('/prev_week')
def prev_week():
    username = auth.authenticate()
    authorize(username, 'admin')
    user = get_user_from_cookies()

    # for now everything is under coursenum 1
    summary, dates = backend_admin.weekly_summary("1", today=today()-timedelta(days=7))
    if summary == False:
        html_code = flask.render_template('error_handling/db_error.html')
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('admin/weekly_summary.html', summary=summary, user=user, dates=dates, names=netids_to_names)
    response = flask.make_response(html_code)
    return response

@app.route('/tutor_overview')
def tutor_overview():
    username = auth.authenticate()
    authorize(username, ['student', 'admin'])
    user = get_user_from_cookies()
    users = db_queries.get_user_info({"user_type": "tutor", "coursenum": "1"})
    if len(users) > 0 and users[0] == False:
        html_code = flask.render_template('error_handling/db_error.html')
        response = flask.make_response(html_code)
        return response
    
    names_bios = {}
    for curr_user in users:
        name = curr_user.get_name()
        netid = curr_user.get_netid()
        bio = db_queries.get_tutor_bio(netid)
        if len(bio) > 0 and bio[0] == False:
            html_code = flask.render_template('error_handling/db_error.html')
            response = flask.make_response(html_code)
            return response
        names_bios[name] = bio

    html_code = flask.render_template('admin/tutor_overview.html', names_bios=names_bios, user=user)
    response = flask.make_response(html_code)
    return response

@app.route('/add_users')
def add_users():
    username = auth.authenticate()
    authorize(username, 'admin')

    html_code = flask.render_template('admin/add_users.html')
    response = flask.make_response(html_code)
    return response

@app.route('/upload', methods=["POST"])
def upload():
    global admin_ids, tutor_ids, student_ids, netids_to_names
    username = auth.authenticate()
    authorize(username, 'admin')
    # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    user_type = flask.request.form['user_type']
    uploaded_file = flask.request.files['users_file']
    filename = uploaded_file.filename
    if filename == '' or os.path.splitext(filename)[-1] != '.csv':
        title = 'Error'
        message = 'Please upload a valid .csv file.'
    else:
        title, message = backend_admin.import_users(uploaded_file, user_type, "1")

    if user_type == "admin":
        admin_ids = utils.get_admin_ids()
    elif user_type == "tutor":
        tutor_ids = utils.get_tutor_ids()
    elif user_type == "student":
        student_ids = utils.get_student_ids()

    netids_to_names = utils.get_names()

    user = get_user_from_cookies()
    html_code = flask.render_template('admin/upload_confirmation.html', message=message, user=user, title=title)
    response = flask.make_response(html_code)
    return response

@app.route('/add_appointment')
def add_appointment():
    username = auth.authenticate()
    authorize(username, 'tutor')
    tutor = flask.request.args.get('tutor_netid')
    date = flask.request.args.get('date')
    user = get_user_from_cookies()

    html_code = flask.render_template('tutor/add_appointment.html', user=user, tutor=tutor, date=date)
    response = flask.make_response(html_code)
    return response

@app.route('/add_appt_submit', methods=['POST'])
def add_appt_submit():
    username = auth.authenticate()
    authorize(username, 'tutor')
    date = flask.request.form['date']
    hour = int(flask.request.form['hour'])
    minute = flask.request.form['minute']
    ampm = flask.request.form['ampm']
    tutor = flask.request.form['tutor']
    location = flask.request.form['location']

    # Convert to 24-hour format
    if ampm == "PM" and hour != 12:
        hour += 12
    elif ampm == "AM" and hour == 12:
        hour = 0
    
    time_str = f"{hour:02d}:{minute}"
    datetime_str = f"{date} {time_str}"
    appt_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
   
    db_modify.add_appointment(appt_time, tutor)

    user = get_user_from_cookies()
    return flask.redirect(flask.url_for('tutorview', netid=user[2]))

@app.route('/cancel_appointment')
def cancel_appointment():
    username = auth.authenticate()
    authorize(username, ['tutor', 'student'])
    time = flask.request.args.get('time')
    tutor = flask.request.args.get('tutor_netid')
    user = get_user_from_cookies()
    
    time = datetime.strptime(time, '%Y-%m-%d %H:%M')

    # Find the appointment
    appts = db_queries.get_appointments({"tutor_netid": tutor, "exact_time": time})
    if len(appts) > 0 and appts[0] == False:
        html_code = flask.render_template('error_handling/db_error.html')
        response = flask.make_response(html_code)
        return response
    
    db_modify.cancel_appointment(time, tutor)

    if SEND_MAIL:
        appt = appts[0] # should only match one appointment
        tutor = db_queries.get_user_info({"netid": appt.get_tutor_netid(), "user_type": "tutor"})[0]
        student = db_queries.get_user_info({"netid": appt.get_student_netid(), "user_type": "student"})[0]

        if user[2] == tutor.get_netid():
            mail_sender.cancel_appointment(appt, tutor, student)
        elif user[2] == student.get_netid():
            mail_sender.cancel_appointment(appt, student, tutor)

    user = get_user_from_cookies()
    html_code = flask.render_template('student/cancel_confirmation.html', user=user)
    response = flask.make_response(html_code)
    return response

@app.route('/edit_appointment', methods=['POST'])
def edit_appointment():
    username = auth.authenticate()
    authorize(username, 'tutor')
    prev_date = flask.request.form['prev-date']
    prev_time = flask.request.form['prev-time']

    tutor = flask.request.form['tutor_netid']
    new_date = flask.request.form['new-date']
    new_time = flask.request.form['new-time']
    
    datetime_str = f"{new_date} {new_time}"
    new_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

    datetime_str = f"{prev_date} {prev_time}"
    prev_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
   
    db_modify.modify_appointment_time(prev_time, new_time, tutor)

    user = get_user_from_cookies()
    return flask.redirect(flask.url_for('tutorview', netid=user[2]))

@app.route('/delete_appointment')
def delete_appointment():
    username = auth.authenticate()
    authorize(username, 'tutor')
    time = flask.request.args.get('time')
    tutor = flask.request.args.get('tutor_netid')
    user = get_user_from_cookies()
    
    time = datetime.strptime(time, '%Y-%m-%d %H:%M')
    db_modify.delete_appointment(time, tutor)

    return flask.redirect(flask.url_for(f"{user[1]}view", netid=user[2]))

# assisted by chatGPT for this function
@app.route('/generate_ics')
def generate_ics():
    time = flask.request.args.get('time')
    tutor = flask.request.args.get('tutor')

    start_time = datetime.strptime(time, '%Y%m%dT%H%M%SZ')

    end_time = start_time + timedelta(minutes=30)

    cal = Calendar()
    cal.add('prodid', '-//ECO100//Appointment//EN')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', 'ECO100 Tutoring with ' + tutor)
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    cal.add_component(event)

    headers = {
        'Content-Type': 'text/calendar',
        'Content-Disposition': 'attachment; filename="appointment.ics"'
    }

    return cal.to_ical(), 200, headers
