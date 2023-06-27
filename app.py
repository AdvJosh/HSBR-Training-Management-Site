"""
This was first written to allow viewing sessions and signing in for 
sessions for the in-house Forbes travel guide training we brought in.
Please note that Forbes travel guide in no way acknowledges,
supports, or endorses anything in this project. 

Now this is morphing in to a basic training management system
that I will contenue to write and impove on as I have time.
I will be entirely rebasing the code from here on out, so 
if you want the final Forbes training version, you want 
to pull commit d1152e1.

This is public because I like open source things, so I feel it is
only fair that I make most of the things I make open source too.
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
  make_response,
  Markup
)
from database import * #  Bring in database related functions
from myfunctions import * # Bring in various other functions
import os
from dotenv import load_dotenv

# Load enviromental variables
load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']
ADMIN_COOKIE_NAME = os.environ['ADMIN_COOKIE_NAME']

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
  page_title = 'HSBR Training Portal Home'
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
          resp.set_cookie('EmpID',EmpID,43200)
          return resp
    except ValueError:
      error = 'The fields should only contain numbers. Please try logging in again.'
  return render_template('login.html',
                        page_title = page_title,
                        login_status = login_status,
                        error=error)


# Let's set up a log-out route
@app.route("/logout")
def logout():
  resp = make_response(redirect('/'))
  resp.delete_cookie('EmpID')
  return resp

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
  signed_in_bool = check_sign_in_status(int(ClassID),int(EmpID))
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  session = load_single_session_from_db(ClassID)
  return render_template('sessionpage.html',
                        session = session,
                        login_status = login_status,
                        attended = signed_in_bool)


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
        if session_signin_result['valid'] == False and session_signin_result['debug'] == 'Couldnt find class':
          error = 'Session Code Invalid! Please double check the session code you entered and try again.'
        elif session_signin_result['valid'] == False and session_signin_result['debug'] == 'Duplicate':
          error = 'You have already signed in for this session previously. You are good to go!'
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


"""
#-#-#-#-#-#-#-#-#-#
    Admin Tools
#-#-#-#-#-#-#-#-#-#
"""
@app.route("/admin/no-access")
def noaccess():
  return render_template('/admin/no-access.html')

#TODO make this better
# A landing page for any admin tools, like the home page but for cool people
@app.route("/admin")
def admin_landing_page():
  page_title = "Admin Tools"
  EmpID = request.cookies.get('EmpID')
  admin_access = request.cookies.get(ADMIN_COOKIE_NAME)
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  if admin_access == None:
    return redirect('/admin/no-access')
  elif admin_access == True:
    admin_access = True    
  page_title = 'ADMIN: Landing Page'
  return render_template('/admin/admin-landing-page.html',
                        page_title = page_title,
                        login_status = login_status,)


# Let's set up the a page for admins to sign associates into sessions
@app.route("/admin/session-signin", methods=['GET', 'POST'])
def admin_sessionsignin():
  EmpID = request.cookies.get('EmpID')
  admin_access = request.cookies.get(ADMIN_COOKIE_NAME)
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  if admin_access == None:
    return redirect('/admin/no-access')
  elif admin_access == True:
    admin_access = True    
  page_title = 'ADMIN: Session Sign In'
  error = None
  sign_in_message = None
  if request.method == 'POST':
    try:
      if len(request.form['SessionCode']) != 4:
        error = 'Session Code should be 4 characters long, you typed '\
        + str(len(request.form['SessionCode'])) + ' characters. Try again.'
      if len(request.form['EmpID']) != 5:
        error = 'Employee ID should be 5 characters long, you typed '\
        + str(len(request.form['EmpID'])) + ' characters. Try again.'
      else:
        session_code = request.form['SessionCode']
        form_EmpID = request.form['EmpID']
        session_signin_dict = {'EmpID' : form_EmpID, 'SessionCode' : session_code.upper()}
        session_signin_result = session_sign_in_to_db(session_signin_dict)
        if session_signin_result['valid'] == False and session_signin_result['debug'] == 'Couldnt find class':
          error = 'Session Code Invalid! Please double check the session code you entered and try again.'
        elif session_signin_result['valid'] == False and session_signin_result['debug'] == 'Duplicate':
          error = 'This associate is already signed in for this session!'
        else:
          sign_in_message = '&nbsp;&nbsp;You have sucsessfully added a sign in record! <br> ID: '\
          + str(form_EmpID) + '<br> to the class with a name of: '\
          + session_signin_result['ClassName']
    except ValueError as e:
      error = e+'Their was an error with what you entered. Please try logging in again.'
  return render_template('/admin/session-signin.html',
                        page_title = page_title,
                        login_status = login_status,
                        error = error,
                        sign_in_successs = Markup(sign_in_message))



# A page to let admins look up an associate
@app.route('/admin/associate-lookup', methods=['GET', 'POST'])
def associate_lookup():
  EmpID = request.cookies.get('EmpID')
  admin_access = request.cookies.get(ADMIN_COOKIE_NAME)
  emp_lookup_result = None
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  if admin_access == None:
    return redirect('/admin/no-access')
  elif admin_access == True:
    admin_access = True    
  page_title = 'ADMIN: Associate Lookup'
  error = None
  if request.method == 'POST':
    try:
      input = str(request.form['EmpName'])
      if not input.isalpha():
        error = 'Name search string should ONLY contain alphabetical characters.'
      else:
        emp_lookup_dict = {'EmpName' : input}
        emp_lookup_result = emp_db_lookup(emp_lookup_dict)
        if len(emp_lookup_result) == 0:
          error = 'No results were returned... Please try a different name to search for.'
    except ValueError as e:
      error = e+'Their was an error with what you entered. Please try again.'
  return render_template('/admin/associate-lookup.html',
                        page_title = page_title,
                        login_status = login_status,
                        error = error,
                        emp_lookup_result = emp_lookup_result)


# Now, let's run the dev server on every available interface
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)