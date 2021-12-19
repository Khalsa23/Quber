from app_folder import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """
    A class model for defining what the User table will look like.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(80))
    emailConformation=db.Column(db.Boolean , default = False)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password, method='sha256')


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_time=db.Column(db.DateTime)
    creatorid=db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(100))
    guestName = db.Column(db.String(30))

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    appoitmentDate=db.Column(db.String(100))
    starttime=db.Column(db.DateTime)
    endtime=db.Column(db.DateTime)
    timeSlots=db.Column(db.Integer)


from app_folder import login_manager

@login_manager.user_loader
def load_user(user_id):
    """ Gets user from the database
    Parameters
    ---------
        name: user_id
        type: int
    Returns
    -------
        It returns users with id user_id
    """
    return User.query.get(int(user_id))