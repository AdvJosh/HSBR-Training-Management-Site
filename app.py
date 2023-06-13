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
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for
from database import * #  Bring in database related functions
from myfunctions import * # Bring in various other functions

# Set up the Flask app
app = Flask(__name__)

login_status = True

# For Testing Use
EmpID = 49080

# Creating a function to get the current time/date in CST


# Let's define the home route
@app.route("/")
def home():
  page_title = 'HSBR Forbes Training Home'
  return render_template('home.html',
                        page_title = page_title,
                        login_status = login_status)


# Let's set up the login route
@app.route("/login")
def login():
  page_title = 'Log in page'
  return render_template('login.html',
                        page_title = page_title,
                        login_status = login_status)


# Let's set up the all sessions route
@app.route("/sessions")
def allsessions():
  page_title = 'All Sessions'
  sessions = load_sessions_from_db()
  return render_template('allsessions.html',
                        page_title = page_title,
                        login_status = login_status,
                        current_date_time = get_current_cst_time(),
                        sessions = sessions)


@app.route('/sessions/<ClassID>')
def sessionpages(ClassID):
  session = load_single_session_from_db(ClassID)
  return render_template('sessionpage.html',
                        session = session,
                        login_status = login_status)


# Let's set up the your sessions page
@app.route("/mysessions")
def mysessions():
  page_title = 'My Sessions'
  sessions = load_sessions_for_one_person(EmpID)
  return render_template('mysessions.html',
                        page_title = page_title,
                        login_status = login_status,
                        current_date_time = get_current_cst_time(),
                        sessions = sessions)


# Let's set up the session sign up page
@app.route("/sign-in")
def sessionsignin():
  page_title = 'Session Sign In'
  return render_template('sessionsignin.html',
                        page_title = page_title,
                        login_status = login_status)


# Now, let's run the dev server on every available interface
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)