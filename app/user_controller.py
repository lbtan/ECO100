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
def tutor():
    appointments = db_tutor.get_times_tutors()
    # user id info
    #TODO fetch info from CAS
    user = ("Hermione Granger", 'tutor', 'hgranger')
    # Parse db results
    apt_tutor = utils.appointments_by_tutor(appointments, user[2])
    apt_times = utils.appointments_by_time(appointments)
    html_code = flask.render_template('tutorview.html', appointments_by_date=apt_times, user=user, apt_tutor=apt_tutor)
    response = flask.make_response(html_code)
    return response

@app.route('/adminview')
def adminview():
    appointments = db_tutor.get_times_tutors()
    apt_times = utils.appointments_by_time(appointments)
    user  = ('Dumbledore', 'admin', 'dmbd')

    html_code = flask.render_template('adminview.html', user=user, appointments_by_date=apt_times)
    response = flask.make_response(html_code)
    return response
