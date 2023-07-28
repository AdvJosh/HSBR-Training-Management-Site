from flask import (
    Blueprint,
    request,
    render_template,
    redirect)


# Defining a blueprint
core_bp = Blueprint(
    'core_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Let's define the home route
@core_bp.route("/")
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
