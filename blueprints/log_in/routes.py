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
log_in_bp = Blueprint(
    'log_in_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


# Let's set up the login route
@log_in_bp.route("/login", methods=['GET', 'POST'])
def login():
  login_status = False
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
          login_status = True
    except ValueError:
      error = 'The fields should only contain numbers. Please try logging in again.'
  return render_template('login.html',
                        page_title = page_title,
                        login_status = login_status,
                        error=error)


# Let's set up a log-out route
@log_in_bp.route("/logout")
def logout():
  resp = make_response(redirect('/'))
  resp.delete_cookie('EmpID')
  login_status = False
  return resp