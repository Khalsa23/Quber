from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TimeField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """
    A Class that defines the login form with username,password and rember feild.
    """
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    """
    A Class that defines the registration form with email,username and password.
    """
    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    password2 = PasswordField(
        'Re-enter Password', validators=[InputRequired()])


class AddAvailability(FlaskForm):
    """
    A class that defines timeslots
    """
    dates=SelectField('Select Date',choices=[])
    start = StringField("Start time", validators=[InputRequired()])
    end = StringField("End time", validators=[InputRequired()])
    slotTime = SelectField('Length of Meetings', validators=[InputRequired()], choices=[
                           (15, '15mins'), (30, '30mins'), (60, '60mins')])
    submit = SubmitField('Set')


class AddAppointment(FlaskForm):
    """
    A class that defines timeslots
    """

    # start = StringField("Start time", validators=[InputRequired()])
    # end = StringField("End time", validators=[InputRequired()])
    appointmentTime=SelectField('Time',choices=[])
    description = StringField('Description', validators=[InputRequired()])
    guestName = StringField('Guest Name', validators=[InputRequired()])
    submit = SubmitField('Set')


class DeleteUserForm(FlaskForm):
    yes = StringField("Yes or No", validators=[InputRequired()])
    delete = SubmitField('Delete')


class EmailNotification(FlaskForm):
    emailConformation = StringField("Email Notification", validators=[InputRequired()])
    delete = SubmitField('Set')
