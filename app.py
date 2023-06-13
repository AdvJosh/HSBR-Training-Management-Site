"""
Written to allow viewing sessions and signing in for sessions
for the in-house Forbes travel guide training we are bringing
in. Please note that Forbes travel guide in no way acknowledges,
supports, or endorses anything in this project. 

This is public because I need it to be to work with replit, but 
once development is complete, it will be moved back to private.
If you can learn something from it, great, but note that this is
not really intended for anything but my particular use-case.

Written By: Joshua Muth
Contact Me: jmuth.com
"""

# Let's bring in the good stuff
from flask import (
  Flask, 
  render_template, 
  jsonify, 
  request, 
  send_from_directory, 
  url_for,
  redirect,
  make_response
)
from database import * #  Bring in database related functions
from myfunctions import * # Bring in various other functions
import os
from dotenv import load_dotenv

# Load enviromental variables
load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']

# Set up the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_status = False

# Creating a function to get the current time/date in CST


# Let's define the home route
@app.route("/")
def home():
  EmpID = request.cookies.get('EmpID')
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  page_title = 'HSBR Forbes Training Home'
  return render_template('home.html',
                        page_title = page_title,
                        login_status = login_status)


# Let's set up the login route
@app.route("/login", methods=['GET', 'POST'])
def login():
  page_title = 'Log in page'
  error = None
  if request.method == 'POST':
    try:
      if len(request.form['EmpID']) != 5:
        error = 'Employee ID should be 5 characters long, you typed '\
        + str(len(request.form['EmpID'])) + ' characters. Try again.'
      if len(request.form['BirthYear']) != 4:
        error = 'Year of Birth should be 4 characters, you typed '\
        + str(len(request.form['BirthYear'])) + ' characters. Try again.'
      else:
        login_dict = {'EmpID' : int(request.form['EmpID']), 'BirthYear' : int(request.form['BirthYear'])}
        login_result = verify_login_from_db(login_dict)
        if login_result['valid'] == False:
          error = 'Invalid Credentials. Please try again.'
        else:
          EmpID = str(login_result['EmpID'])
          resp = make_response(redirect('/'))
          resp.set_cookie('EmpID',EmpID,7800)
          return resp 
    except ValueError:
      error = 'The fields should only contain numbers. Please try logging in again.'
  return render_template('login.html',
                        page_title = page_title,
                        login_status = login_status,
                        error=error)


# Let's set up the all sessions route
@app.route("/sessions")
def allsessions():
  EmpID = request.cookies.get('EmpID')
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  page_title = 'All Sessions'
  sessions = load_sessions_from_db()
  return render_template('allsessions.html',
                        page_title = page_title,
                        login_status = login_status,
                        current_date_time = get_current_cst_time(),
                        sessions = sessions)


@app.route('/sessions/<ClassID>')
def sessionpages(ClassID):
  EmpID = request.cookies.get('EmpID')
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  session = load_single_session_from_db(ClassID)
  return render_template('sessionpage.html',
                        session = session,
                        login_status = login_status)


# Let's set up the your sessions page
@app.route("/mysessions")
def mysessions():
  EmpID = request.cookies.get('EmpID')
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  page_title = 'My Sessions'
  sessions = load_sessions_for_one_person(EmpID)
  return render_template('mysessions.html',
                        page_title = page_title,
                        login_status = login_status,
                        current_date_time = get_current_cst_time(),
                        sessions = sessions)


# Let's set up the session sign up page
@app.route("/sign-in", methods=['GET', 'POST'])
def sessionsignin():
  EmpID = request.cookies.get('EmpID')
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  page_title = 'Session Sign In'
  error = None
  sign_in_message = None
  if request.method == 'POST':
    try:
      if len(request.form['SessionCode']) != 4:
        error = 'Session Code should be 4 characters long, you typed '\
        + str(len(request.form['SessionCode'])) + ' characters. Try again.'
      else:
        session_code = request.form['SessionCode']
        session_signin_dict = {'EmpID' : EmpID, 'SessionCode' : session_code.upper()}
        session_signin_result = session_sign_in_to_db(session_signin_dict)
        if session_signin_result['valid'] == False:
          error = 'Session Code Invalid or you are already signed in for this session. Please try again.'
        else:
          sign_in_message = 'You have sucsessfully signed in for: '\
          + session_signin_result['ClassName'] + '!'
    except ValueError as e:
      error = e+'Their was an error with what you entered. Please try logging in again.'
  return render_template('sessionsignin.html',
                        page_title = page_title,
                        login_status = login_status,
                        error = error,
                        sign_in_successs = sign_in_message)


# Now, let's run the dev server on every available interface
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)