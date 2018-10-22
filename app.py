import os
import json
from bson import json_util
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'brewjar'
app.config['MONGO_URI'] = 'mongodb://admin:99Prism@ds149732.mlab.com:49732/brewjar'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-account')
def add_user():
    
#     if request.method == ['POST']:
#         hashed_password = bcrypt.generate_password_hash(request.form['password']).decode(utf-8)
#         user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
#         mongo.db.user.insert_one(user)
    
    return render_template('createaccount.html')

@app.route('/sign-in')
def signin():
    # _user = mongo.db.user.findOne()
    # valid_user = [user for user in _user]
    
    # if request.method == 'POST':
    #     error = None
    #     if request.form['email'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'The username and password do not match. Try again, or create an account'
    #     else:
    #         return redirect(url_for('home'))
            
    return render_template('signin.html')

@app.route('/home')
def home():
    collection = mongo.db.brew
    all_brews = collection.find_one()
    return render_template('home.html', all_brews=all_brews)

@app.route('/choose-a-brew')
def choose_a_brew():
    return render_template('filterform.html') 
        
@app.route('/brew-results', methods=['GET','POST'])
def get_filter_results():
    #get DB collection 
    allbrews = mongo.db.brew
    
    # # initialize empty list to store form data
    # brew_choice_list = []
    # stufffree_list = []
    # # level = ''
    
    #get form submissions
    stufffree = request.form.get('stuff-free')
    level = request.form.get('level')
    brew_types = request.form.get('brew-type')
    
    # #append to lists
    # brew_choice_list.append(brew_types)
    # stufffree_list.append(stufffree)
    # # level.append(level)
    
    filter_results = allbrews.find({"recipe_profile.cat_name": brew_types,"recipe_profile.level": level})
    
    f = filter_results.to_dict()

    return render_template('brewresults.html', f=f)
    
# @app.route('/success')
# def success():
#     return render_template('success.html')

@app.route('/return_all')
def return_all():
    db = mongo.db.brew;

    documents = db.find({"recipe_profile.cat_name":"beer"})
    
    
    # ({"category_1.id_alc": ObjectId("d4a2b4ab7c0aa0388de410d4")},{"category_1.alcohol": {"$elemMatch": {"level":'beginner', "cat_name":"wine", "free-from":"gluten-free"}})]
    return json_util.dumps({'cursor': documents}) 
    
@app.route('/add-profile')
def add_profile():
    return render_template('addbrewProfile.html')

@app.route('/add-recipe')
def add_recipe():
    return render_template('addbrewRecipe.html')

@app.route('/my-brews') 
def my_brews():
    return render_template('mybrews.html')
    
@app.route('/insert-brew', methods=['POST'])
def insert_brew():
    brews = mongo.db.brew
    
    # return form field submissions from addBrewProfile

    recipe_name = request.form['recipe_name']
    author_name = request.form['author_name']
    recipe_description = request.form['recipe_description']
    category_name = request.form['cat-name']
    style = request.form['style']
    flavour = request.form['flavour']
    # level = request.form['level']
    # region = request.form['region']
    method = request.form['method']
    freefrom = request.form['free-from']
    properties = request.form['properties']

    # add user input to the brew collection
    
    # brews.insert_one({"_id": ObjectId("5bc53e0ce7179a4377fb226e")},
    # {"$addToSet": 
    #     {"category.alcohol":
    #         {
    #         "cat_name": category_name,
    #         "recipe_name": recipe_name,
    #         "style": style,
    #         # "level": level,
    #         "flavour": flavour,
    #         # "region": region,
    #         "method": method,
    #         "properties": properties,
    #         "free-from": freefrom
    #         }
    #     }
    # })
    
    # brews.insert_one(request.form.to_dict())
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)