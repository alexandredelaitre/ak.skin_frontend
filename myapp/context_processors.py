from flask_login import current_user

def inject_current_user():
    return {'current_user': current_user}