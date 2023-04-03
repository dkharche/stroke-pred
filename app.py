#importing the necessary libraries
from flask import Flask, render_template, redirect, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from pymongo import MongoClient
from flask_pymongo import PyMongo
import bcrypt



app = Flask(__name__, template_folder='template')
client = MongoClient("mongodb+srv://divijkharche01:LEATHERbat01@cluster0.g4wwula.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('db')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        users = db.user
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('home'))

        return 'That username already exists!'

    return render_template('register.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = db.user_data
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            else:
                return 'Invalid username/password combination'

        return 'Invalid username/password combination'

    return render_template('login.html')

@app.route('/success')
def success():
    if 'username' in session:
        return render_template('stroke.html', username=session['username'])

    return redirect(url_for('login'))

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))
#
if __name__ == '__main__':
    app.run(debug=True)

# #Running the application
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)