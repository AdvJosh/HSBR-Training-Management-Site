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


# Let's define the home route
@app.route("/")
def home():
  page_title = 'HSBR Forbes Training Home'
  return render_template('home.html',
                        page_title = page_title)


# Now, let's run the dev server on every available interface
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)