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
from flask import Flask, render_template, jsonify, request

# Set up the Flask app
app = Flask(__name__)

login_status = True

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
  return render_template('allsessions.html',
                        page_title = page_title,
                        login_status = login_status)


# Let's set up the your sessions page
@app.route("/mysessions")
def mysessions():
  page_title = 'My Sessions'
  return render_template('mysessions.html',
                        page_title = page_title,
                        login_status = login_status)


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