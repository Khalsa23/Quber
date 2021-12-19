How to run our program:

Requirement:
Python, VSCODE(or Pycharm), flask installed

Flask Installation click here: 
https://flask.palletsprojects.com/en/1.1.x/installation/

We used flask-full calander to generate file https://github.com/kkarimi/flask-fullcalendar

1.Download the project package

2.Open the project package on your IDE

3.Within the project folder run the following on the terminal run the following:

  >>> activate virtual env

        On Windows:
              venv\Scripts\activate

        On Mac
          . venv/bin/activate

   >>> python run.py
     
4.Make sure you can find app.db generated after the above.If there is not app.db

   >>> cd project

   >>> python
   
   >>>from app_folder import db 
   
   >>> db.create_all()

5.Open Terminal and type python run.py

6.The output should be like this:
 warnings.warn(FSADeprecationWarning(
 * Serving Flask app "app_folder" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 
7. Copy and paste the link above to get to the homepage of Quber

General Instructions on using Quber:

-When you first enter Quber, you will be taken to the home page. Click login if you already have a Quber account or click the register link to be taken to the create account page to sign up for Quber. If you click the login link, but don't have an account,  just click the register link in the login page.

Creating Account:
1.Username length have to be at least 4 characters.
2. The Password length you set has to be at least 8 characters.
Log Out:
1.When you log out from the dashboard of QUBER, you will be redirected to the home page. 

Db_check.py:

-run this class to check the database after creating an account with Quber or to check current users on quber. We have this class to make sure the database works and that the set password func is changing the passwords to hashes in order to guard user passwords. 
