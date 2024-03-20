#-----------------------------------------------------------------------
# user_controller.py
# Authors: Libo Tan
# 
#
# Handles the logic of different views.
#-----------------------------------------------------------------------

import flask

#----------------------------------------------------------------------#

app = flask.Flask(__name__, template_folder = 'app/templates')

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
    html_code = flask.render_template('tutorview.html')
    response = flask.make_response(html_code)
    return response

@app.route('/adminview')
def adminview():
    html_code = flask.render_template('adminview.html')
    response = flask.make_response(html_code)
    return response
