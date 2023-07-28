from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    Markup,
    make_response)
from dotenv import load_dotenv
from database import * #  Bring in database related functions
from myfunctions import * # Bring in various other functions
import os


# Defining a blueprint
sessions_bp = Blueprint(
    'sessions_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Let's set up the all sessions route
@sessions_bp.route("/all-sessions")
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


@sessions_bp.route('/session-info/<ClassID>')
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
@sessions_bp.route("/mysessions")
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
@sessions_bp.route("/sign-in", methods=['GET', 'POST'])
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
