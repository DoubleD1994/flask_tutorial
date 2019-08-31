from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/daviddryburgh/Documents/Programming/Python/flask_tutorial/database.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
