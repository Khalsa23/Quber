from datetime import datetime, date
import json
import datetime
from flask import render_template, redirect,request,jsonify,url_for,flash
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
from app_folder.forms import LoginForm, RegisterForm, AddAvailability, AddAppointment, DeleteUserForm,EmailNotification
from app_folder import app, db
from .models import User, Appointments, Availability
# https://github.com/kkarimi/flask-fullcalendar

def timeSlots(start_time, end_time, slot_time):
    hours = []
    while start_time <= end_time:
        hours.append(start_time.strftime("%I:%M %p"))
        start_time += datetime.timedelta(minutes=slot_time)
    return hours

def nextSevenDays():
    newDates=[]
    base = datetime.datetime.today().date()
    for x in range(0, 7):
        new=base + datetime.timedelta(days=x)
        newDates.append(new.strftime('%Y-%m-%d'))
    return newDates

# @app.route('/')
# def home():
#     """ This is the Home route renders the homepage.
#     Parameters
#     ----------
#         No parameters required.
#     Returns
#     --------
#         It renders the home.html template.
#     """
#     return render_template('home.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ This is the Login route it renders the loginpage.

    Parameters
    ----------
        Methods
            GET:/login 
                Renders the login form page.
            POST:/login
                Submits the data from the form.
    Returns
    --------
        It renders the login.html template
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            flash('Wrong credentials')
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('You were successfully logged in')
                return redirect('/dashboard')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ 
    This is the register route it renders the registration page.

    Parameters
    ----------
        Methods
            GET:/register
                Renders the register form page.
            POST:/register
                Submits the data from the register form page.
    Returns
    -------
        It renders the register.html template
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already associated with an account')
        else:
            user = User(username=form.username.data, email=form.email.data,)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Succesfully created account')
            return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    """ 
    This is the Dashboared route it renders the dashboared page.

    Parameters
    ----------
        GET:/dashboard
            Display the dashboared page

    Returns
    -------
        It renders the dashboard.html template

    """
    now = date.today()
    dt_string = now.strftime("%B %d, %Y")
    user = User.query.filter_by(username=current_user.username).first()
    print(user.username)
    appt = Appointments.query.filter_by(creatorid=user.id).order_by(Appointments.appointment_time).all()  
    return render_template('creator.html', name=current_user.username, appointments=appt, todayDate=dt_string)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """ Logs out the user
    Parameters
    ----------
        POST:/logout
            Display the dashboared page

    Returns
    -------
        It redirect the user to the homepage.
    """
    logout_user()
    return redirect('/')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = AddAvailability()
    deleteform = DeleteUserForm()
    emailNotification = EmailNotification()
    form.dates.choices=[(i,i) for i in nextSevenDays()]
    now = form.dates.data
    if form.is_submitted() and form.start.data and form.end.data:
        avl = Availability.query.filter_by(userid=current_user.id).filter_by(appoitmentDate=now).first()
        if avl != None:
            if avl.appoitmentDate == now:
                startingTime = now + ' ' + str(datetime.datetime.strptime(form.start.data, '%H:%M').time())
                endingTime = now + ' ' + str(datetime.datetime.strptime(form.end.data, '%H:%M').time())
                dateStart = datetime.datetime.strptime(startingTime, '%Y-%m-%d %H:%M:%S')
                dateEnd = datetime.datetime.strptime(endingTime, '%Y-%m-%d %H:%M:%S')
                avl.timeSlots=form.slotTime.data
                avl.starttime=dateStart
                avl.endtime=dateEnd
                db.session.commit()
                flashString=('Availability Updated for {}'.format(now))
                flash(flashString)

        else:
            startingTime = now + ' ' + str(datetime.datetime.strptime(form.start.data, '%H:%M').time())
            print(startingTime)
            endingTime = now + ' ' + str(datetime.datetime.strptime(form.end.data, '%H:%M').time())
            dateStart = datetime.datetime.strptime(startingTime, '%Y-%m-%d %H:%M:%S')
            dateEnd = datetime.datetime.strptime(endingTime, '%Y-%m-%d %H:%M:%S')
            availability = Availability(userid=current_user.id, appoitmentDate=now,starttime=dateStart, endtime=dateEnd,timeSlots = form.slotTime.data)
            db.session.add(availability)
            db.session.commit()
            flashString=('Availability Added for {}'.format(now))
            flash(flashString)

    elif deleteform.is_submitted():
        formData=deleteform.yes.data.lower()
        if formData == 'yes':
            User.query.filter_by(id=current_user.id).delete()
            db.session.commit()
            flash('Account deleted')
            return redirect('/login')
    if emailNotification.is_submitted():
        eData=emailNotification.emailConformation.data.lower()
        if eData == 'yes':
            user=User.query.filter_by(id=current_user.id).first()
            print(user.emailConformation)
            user.emailConformation = True
            db.session.commit()
            flash('Email conformation set to YES')
            return redirect('/settings')
        if eData == 'no':
            user=User.query.filter_by(id=current_user.id).first()
            user.emailConformation = False
            db.session.commit()
            flash('Email conformation set to NO')
            return redirect('/settings')
    return render_template('settings.html', form=form ,deleteform=deleteform,emailNotification=emailNotification)


@app.route('/<userName>', methods=['GET', 'POST'])
def appointments(userName):
    newSlot=[]
    avalability=[]
    flag=False
    requestedDate=request.args.get('rDate')
    form = AddAppointment()
    user = User.query.filter_by(username=userName).first()
    if user == None:
        flash('User not found')
        return redirect('/')
    if requestedDate != None:
        now=datetime.datetime.strptime(requestedDate , '%Y-%m-%d').date()
        avalability=Availability.query.filter_by(appoitmentDate=requestedDate).filter_by(userid=user.id).first()
        if avalability:
            flag=True
            newSlot = timeSlots(avalability.starttime, avalability.endtime, avalability.timeSlots) 
            return jsonify(slots=newSlot)
        else:
            flash('Creator didnt set time for this date')
    if form.is_submitted():
        print('yes')
        newDate=str(datetime.datetime.strptime(str(date.today()) , '%Y-%m-%d').date()) + ' '+str(datetime.datetime.strptime(form.appointmentTime.data, '%H:%M %p').time())
        convertedDate = datetime.datetime.strptime(newDate, '%Y-%m-%d %H:%M:%S')
        appt = Appointments.query.filter_by(appointment_time=convertedDate).filter_by(creatorid=user.id).all()
        if appt:
            flash('Time already taken.Please chose another time')
            return redirect(url_for('appointments',userName=userName))
        else:
            user = User.query.filter_by(username=userName).first()
            print(user.id)
            appt = Appointments(appointment_time=convertedDate,creatorid=user.id,description=form.description.data, guestName=form.guestName.data)                        
            db.session.add(appt)
            db.session.commit()
            flash('Appoitment booked')
    return render_template('appoitments.html', form=form,userName=userName,flag=flag)
    
    

@app.route('/getAppointments/<userName>', methods=['POST'])
def getSlots(userName):
    requestedDate=request.get_json() 
    return redirect(url_for('appointments',rDate=requestedDate,userName=userName))
