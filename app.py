#importing the necessary libraries
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

#configuring the application

app = Flask(__name__ ,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#Initializing the database
db = SQLAlchemy(app)

#Creating the database table (user)
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    EmailID = db.Column(db.String(80))
    password = db.Column(db.String(80))

#Creating the home page
@app.route('/')
def home():
    return render_template('home.html')
    

#Creating the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        EmailID = request.form['EmailID']
        password = request.form['password']
        user = User.query.filter_by(EmailID=EmailID, password=password).first()
        if user:
            return redirect(url_for('success'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

#Creating the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        EmailID = request.form['EmailID']
        password = request.form['password']
        user = User(EmailID=EmailID, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

#Creating the success page
@app.route('/success')
def success():
    return render_template('success.html')

#Creating the Google sign in page
@app.route('/google_login')
def google_login():
    return render_template('google_login.html')

#Running the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)