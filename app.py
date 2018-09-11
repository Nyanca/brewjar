import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'brewjar-app'
app.config['MONGO_URI'] = 'mongodb://admin:99Prism@ds225382.mlab.com:25382/brewjar_app'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/create-account')
def add_user():
    if request.method == ['POST']:
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode(utf-8)
        user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
        mongo.db.user.insert_one(user)
    
    return render_template('createaccount.html')

@app.route('/sign-in', methods=['POST'])
def signin():
    _user = mongo.db.user.findOne()
    valid_user = [user for user in _user]
    
    if request.method == 'POST':
        error = None
        if request.form['email'] != 'admin' or request.form['password'] != 'admin':
            error = 'The username and password do not match. Try again, or create an account'
        else:
            return redirect(url_for('home'))
            
    return render_template('signin.html', error=error)

@app.route('/home')
def home():
    return render_template('home.html')
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)