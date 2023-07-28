from flask import Blueprint


# Defining a blueprint
user_profiles_bp = Blueprint(
    'user_profiles_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
