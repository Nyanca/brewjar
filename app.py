import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'brewjar'
app.config['MONGO_URI'] = 'mongodb://admin:99Prism@ds149732.mlab.com:49732/brewjar'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# @app.route('/create-account')
# def add_user():
#     if request.method == ['POST']:
#         hashed_password = bcrypt.generate_password_hash(request.form['password']).decode(utf-8)
#         user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
#         mongo.db.user.insert_one(user)
    
#     return render_template('createaccount.html')

# @app.route('/sign-in', methods=['POST'])
# def signin():
#     _user = mongo.db.user.findOne()
#     valid_user = [user for user in _user]
    
#     if request.method == 'POST':
#         error = None
#         if request.form['email'] != 'admin' or request.form['password'] != 'admin':
#             error = 'The username and password do not match. Try again, or create an account'
#         else:
#             return redirect(url_for('home'))
            
#     return render_template('signin.html', error=error)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/choose-a-brew')
def choose_a_brew():
    return render_template('filterform.html') 
        
@app.route('/brew-results', methods=['GET','POST'])
def brew_results():
    all_brews = mongo.db.brew.category.find()
    brew_choices = []
    
    brew_types = request.form.get('brew-type')
    brew_choices.append(brew_types)
    
    def filtermatch(brew_choices):
        if (brew_choices in all_brews):
            return True
        else:
            return False
        
    filter_results = filter(filtermatch, brew_types)
        
    # stufffree = request.form.get('stuff-free')
    # level = request.form.get('level')
   
    return render_template('brewresults.html', filter_results=filter_results)
    
# @app.route('/success')
# def success():
#     return render_template('success.html')

@app.route('/add-profile')
def add_profile():
    return render_template('addbrewProfile.html')

@app.route('/add-recipe')
def add_recipe():
    return render_template('addbrewRecipe.html')

@app.route('/my-brews') 
def my_brews():
    return render_template('mybrews.html')
    
@app.route('/insert-brew')
def insert_brew():
    brews = mongo.db.brew
    brews.insert_one(request.form.to_dict())
    return redirect(url_for('success'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)