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

#-#-#-# Importing all of the blueprints #-#-#-#
from blueprints.admin.routes import admin_bp
from blueprints.log_in.routes import log_in_bp
from blueprints.core.routes import core_bp
from blueprints.sessions.routes import sessions_bp

#-#-#-# Registering blueprints #-#-#-#
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(log_in_bp)
app.register_blueprint(core_bp)
app.register_blueprint(sessions_bp, url_prefix='/sessions')


# Now, let's run the dev server on every available interface
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)