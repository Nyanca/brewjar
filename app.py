import os
import json
import bcrypt
from bson import json_util
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for, jsonify, session, flash, g
from flask_pymongo import PyMongo, ObjectId
from functools import wraps


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'brewjar'
app.config['MONGO_URI'] = 'mongodb://admin:99Prism@ds149732.mlab.com:49732/brewjar'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    users = mongo.db.user
    password = request.form.get('password')
    username = request.form.get('username')
    existing_user = users.find_one({'username': username})
    
    if request.method == 'POST':
        if existing_user is None:
            hashPw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': username, 'password': hashPw, 'mybrews':[]})
            session['username'] = username
            return redirect(url_for('login'))
            
        else:
            flash('*That username already exists')
            return render_template('register.html')

    return render_template('register.html', username=username, password=password)
    
@app.route('/log-in', methods=['POST', 'GET'])
def login():
    users = mongo.db.user
    username = request.form.get('username')
    password = request.form.get('password')
    login_user = users.find_one({'username': username})
    
    session['user'] = username
    
    # passwords aren't being stored porperly & will need encode when stored properly
    if login_user:
        if bcrypt.hashpw(password.encode('utf-8'), login_user['password']) == login_user['password']:
            user_name = username
            return render_template('home.html', username=user_name)
    else:
        flash('*invalid login details')
        return render_template('login.html')
            
    return render_template('login.html')

# @app.route('/get_user')
# # get the user form the session if user exists & login automatically
# def get_user():
#     if 'username' in session:
#         return session['username'] and redirect('home.html')
        
#     return redirect('login.html')

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/choose-a-brew')
def choose_a_brew():
    return render_template('filterform.html') 
        
@app.route('/brew-results', methods=['GET','POST'])
def get_filter_results():
    # get DB collection 
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
    filter_data = allbrews.find()
    
    # filter_data = allbrews.find({"recipe_profile.cat_name": brew_types,"recipe_profile.level": level})

    # f = []
    
    # for brew in filter_data:
    #     f.append(brew)

    return render_template('brewresults.html', filter_data=filter_data, level=level, brew_types=brew_types)
    
@app.route('/success')
def success():
    return render_template('success.html')
    
@app.route('/add-profile')
def add_profile():
    # allows the user to add a new recipe profile via form on addBrewProfile.html
    return render_template('addbrewProfile.html')

@app.route('/add-recipe')
def add_recipe():
     # allows the user to add a new recipe via form on addBrewRecipe.html
    return render_template('addbrewRecipe.html')

@app.route('/my-brews') 
def my_brews():
    return render_template('mybrews.html')
    
# @app.route('/add_vote', methods=['GET','POST'])
# def add_vote():
#     recipe_id = request.form['recipe_id']
#     return render_template('fullview.html', recipe_id=recipe_id)
    
@app.route('/expand_result', methods=['GET','POST'])
# render template fullview.html 
def expand_result():
    recipe_id = request.form.get('recipe_id')
    brew_db = mongo.db.brew
    recipe_item = brew_db.find_one({"_id": ObjectId(recipe_id)})
    
    return render_template('fullview.html', recipe_item=recipe_item, recipe_id=recipe_id)

@app.route('/add_to_myBrews', methods=['GET','POST'])
def add_to_myBrews():
    # get recipe id
    myBrew_id = request.form.get('myBrew_id')
    # get database collections
    user = mongo.db.user
    brew_db = mongo.db.brew
    # get recipe to add to user collection myBrews
    myBrews_entry = brew_db.find_one({"_id": ObjectId(myBrew_id)})
    # get user
    session_user = g.user
    
    # enter recipe into user's recipe dashboard myBrews 
    # user.find_and_modify({
    #     "query": {'username': session_user},
    #     "sort": { 'recipe_profile.cat_name': 1 },
    #     "update":{"$push":{"mybrews": {"_id": ObjectId(myBrew_id)}}} 
    # }) 
    
    user.update({'username': session_user},
        {"$addToSet":{"mybrews": {"_id": ObjectId(myBrew_id)}} }
    ) 
                    
    #insert the above item into the user collection     
    # work on this and figure how to add recipe to user dashboard, maybe store all id's in a list to access them and iterate through each list item
    return render_template('success.html', myBrews_entry = myBrews_entry, myBrew_id=myBrew_id)
        
@app.route('/insert-brew', methods=['GET','POST'])
def insert_brew():
    brews = mongo.db.brew
    
    # return form field submissions from addBrewProfile and addBrewRecipe
    author_name = request.form['author_name']
    category_name = request.form['cat-name']
    recipe_name = request.form['recipe_name']
    recipe_description = request.form['recipe_description']
    style = request.form['style']
    level = request.form['level']
    flavour = request.form['flavour']
    region = request.form['region']
    method = request.form['method']
    properties = request.form['properties']
    freefrom = request.form['free-from']
    # equip_list = request.form['equip_list']
    # ingredients_list = request.form['ingredients_list']
    # prep_method = request.form['prep_method']
   
    
    # need help adding recipe object with arrays to collection and help with converting arrays entries into single string values

    # add user input to the brew collection
    
    brews.insert_one({   
            "author_name": author_name,
            "cat_name": category_name,
            "recipe_name": recipe_name,
            "recipe_description": recipe_description,
            "style": style,
            "level": level,
            "flavour": flavour,
            "region": region,
            "method": method,
            "properties": properties,
            "free-from": freefrom,
            # "recipe":{"$push":
            #             {
            #                 "equip_list": {"$each": [equip_list]}
            #             }
            #         },
            #         {"$push": 
            #             {
            #               "ingredients_list": {"$each": [ingredients_list]}
            #             }
            #         },
            #         {"$push":
            #             {
            #               "prep_method": {"$each": [prep_method]}
            #             }
            #         }
    })
    
    # brews.insert_one(request.form.to_dict())
    return render_template('success.html')

@app.route('/add_to_my_brews', methods=['GET', 'POST'])
def add_recipe_to_user_dashboard():
    a = request.form.get('idid')
    return render_template('success.html', a=a)


if __name__ == '__main__':
    app.secret_key = b'\xeb\xd3\x0c\x89P\xed.\x15~\xa6\xc6\xad;\x16\x8fH'
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)