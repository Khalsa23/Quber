## run this class to check the db database to make sure it is running correctly and holding the values entered
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

with db.engine.connect() as con:
    res = con.execute('SELECT * FROM User')
    print(res.fetchall())