"""
Here lies all of the admin tools. This may morph over time as I rebase the code
to include a better user/class management system
"""


# Bring in the goods
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    Markup)
from dotenv import load_dotenv
from database import * #  Bring in database related functions
from myfunctions import * # Bring in various other functions
import os


# Load enviromental variables
load_dotenv()
ADMIN_COOKIE_NAME = os.environ['ADMIN_COOKIE_NAME']


# Defining a blueprint
admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@admin_bp.route("/no-access")
def noaccess():
  return render_template('no-access.html')



# TODO Make this better and tied to an actual login system
@admin_bp.route('/')
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
    return redirect('no-access')
  elif admin_access == True:
    admin_access = True    
  page_title = 'ADMIN: Landing Page'
  return render_template('admin-landing-page.html',
                        page_title = page_title,
                        login_status = login_status,)


# Let's set up the a page for admins to sign associates into sessions
@admin_bp.route("/session-signin", methods=['GET', 'POST'])
def admin_sessionsignin():
  EmpID = request.cookies.get('EmpID')
  admin_access = request.cookies.get(ADMIN_COOKIE_NAME)
  if EmpID == None:
    return redirect('/login')
  else:
    EmpID = int(EmpID)
    login_status = True
  if admin_access == None:
    return redirect('no-access')
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
  return render_template('session-signin.html',
                        page_title = page_title,
                        login_status = login_status,
                        error = error,
                        sign_in_successs = Markup(sign_in_message))


# A page to let admins look up an associate
@admin_bp.route('/associate-lookup', methods=['GET', 'POST'])
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
    return redirect('no-access')
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
  return render_template('associate-lookup.html',
                        page_title = page_title,
                        login_status = login_status,
                        error = error,
                        emp_lookup_result = emp_lookup_result)