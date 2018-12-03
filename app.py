import os
import json
import bcrypt
from bson import json_util
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for, jsonify, session, flash, g
from flask_pymongo import PyMongo, ObjectId
from functools import wraps

# configure the brewjar database with pymongo
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'brewjar'
app.config['MONGO_URI'] = 'mongodb://admin:99Prism@ds149732.mlab.com:49732/brewjar'

mongo = PyMongo(app)
    
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
    
@app.route('/')
def index():
    # return index.html page
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # add a new user to the user collection by unique username
    users = mongo.db.user
    password = request.form.get('password')
    username = request.form.get('username')
    existing_user = users.find_one({'username': username})
    
    # if the method is post then execute the following else return register page
    if request.method == 'POST':
        
        # ensure the username is unique else see flash message 
        if existing_user is None:
            
            # encrypt the user password for safe storage in the database
            hashPw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': username, 'password': hashPw, 'mybrews':[]})
            # session['username'] = username
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
    valid_user = users.find_one({'username': username})
    
    session['user'] = username
    
    if valid_user:
        if bcrypt.hashpw(password.encode('utf-8'), valid_user['password']) == valid_user['password']:
            user_name = username
            return render_template('home.html', username=user_name)
    else:
        flash('*invalid login details')
        return render_template('login.html')
            
    return render_template('login.html')
    
@app.route('/home')
def home():
    session_user = g.user
    if session_user:
        return render_template('home.html', username=session_user)
    return render_template('login.html')

@app.route('/choose-a-brew')
def choose_a_brew():
    session_user = g.user
    if session_user:
        return render_template('filterform.html', username=session_user) 
    return render_template('login.html')
        
@app.route('/brew-results', methods=['GET','POST'])
def get_filter_results():
    session_user = g.user
    if session_user:
        # get DB collection 
        allbrews = mongo.db.brew

        #get form submissions
        if request.method=='POST':
            free_from = request.form['stuff-free']
            level = request.form['level']
            brew_types = request.form['brew-type']

            filter_data = allbrews.find()

            return render_template('brewresults.html', filter_data=filter_data, level=level, brew_types=brew_types, free_from=free_from, username=session_user)
            
    return render_template('login.html') 
    
@app.route('/success')
def success():
    session_user = g.user
    if session_user:
        return render_template('success.html', username=session_user)
    return render_template('login.html') 
    
@app.route('/add-profile')
def add_profile():
    session_user = g.user
    if session_user:
        # allows the user to add a new recipe profile via form on addBrewProfile.html
        return render_template('addbrewProfile.html', username=session_user)
    return render_template('login.html') 

@app.route('/add-recipe')
def add_recipe():
    session_user = g.user
    
    if session_user:
         # allows the user to add a new recipe via form on addBrewRecipe.html
        return render_template('addbrewRecipe.html', username=session_user)
    return render_template('login.html') 

@app.route('/my-brews') 
def my_brews():
    session_user = g.user
    
    if session_user:
        
        user_doc = mongo.db.user.find_one({'username':session_user})
        
        for k,v in user_doc.items():
            if k == 'mybrews':
            # need to find dynamic way to access all recipe id's in the array
                c = v[1]
                for k,v in c.items():
                    recipe_id = v
                    recipe_doc = mongo.db.brew.find({"_id": ObjectId(recipe_id)})
                    
        return render_template('mybrews.html', user_doc=user_doc, username=session_user, recipe_doc=recipe_doc)
        
    return render_template('login.html') 

@app.route('/edit_recipe', methods=['GET','POST'])
def edit_recipe():
    #gets an instance of the recipe to return recipe form with data
    session_user = g.user
    
    if session_user:
       recipe_id = request.form.get('recipe_doc_id')
       recipe_doc = mongo.db.brew.find_one({"_id": ObjectId(recipe_id)})
       
       return render_template('edit_profile_form.html', recipe_doc=recipe_doc, recipe_id=recipe_id, username=session_user)
        
    return render_template('login.html')
    
@app.route('/update_recipe', methods=['GET','POST'])
def update_recipe():
    #gets updated form data from edit_recipe and updates DB document
    session_user = g.user
    
    if session_user:
        brews = mongo.db.brew
        
        recipe_id = request.form.get('recipe_doc_id')

        # return form field submissions from edit brew profile
        author_name = request.form.get('author_name')
        category_name = request.form.get('cat-name')
        recipe_name = request.form.get('recipe_name')
        recipe_description = request.form.get('recipe_description')
        style = request.form.get('style')
        level = request.form.get('level')
        flavour = request.form.get('flavour')
        region = request.form.get('region')
        method = request.form.get('method')
        properties = request.form.get('properties')
        freefrom = request.form.get('free-from')
        
        brews.update_one({"_id": ObjectId(recipe_id)}, 
                    {"$set":{ 
                        "author": author_name,
                        "recipe_profile":{
                                "cat_name": category_name,
                                "recipe_name": recipe_name,
                                "recipe_description": recipe_description,
                                "style": style,
                                "level": level,
                                "flavour": flavour,
                                "region": region,
                                "method": method,
                                "properties": properties,
                                "free_from": freefrom,
                                "recipe":{
                                "equip_list":[],
                                "ingredients_list":[],
                                "prep_method":[],
                            }
                        }
                     }
                })
       
        return render_template('home.html', username=session_user)
        
    return render_template('login.html')
 
@app.route('/delete_recipe', methods=['GET','POST'])
def delete_recipe():
    #gets an instance of the recipe with id, and deletes that recipe from the database
    session_user = g.user
    
    if session_user:
       recipe_id = request.form.get('recipe_doc_id')
       recipe_doc = mongo.db.brew.remove({"_id": ObjectId(recipe_id)})
       
       return render_template('home.html', username=session_user)
        
    return render_template('login.html')
    
@app.route('/add_vote', methods=['GET','POST'])
def add_vote():
    session_user = g.user
    
    if session_user:
        recipe_id = request.form.get('recipe_id')
        # increment the current vote count in the recipe selected document
        mongo.db.brew.update({"_id":ObjectId(recipe_id)}, 
            {"$inc": 
                {"recipe_profile.upvotes": 1}
            }
        )
        return render_template('brewresults.html', recipe_id=recipe_id, username=session_user)
        
    return render_template('login.html') 
    
@app.route('/expand_result', methods=['GET','POST'])
# render template fullview.html to show full recipe profile and prep instructions
def expand_result():
    session_user = g.user
    
    if session_user:
        recipe_id = request.form.get('recipe_id')
        brew_db = mongo.db.brew
        recipe_item = brew_db.find_one({"_id": ObjectId(recipe_id)})
        
        return render_template('fullview.html', recipe_item=recipe_item, recipe_id=recipe_id, username=session_user)

    return render_template('login.html') 
    
@app.route('/add_to_myBrews', methods=['GET','POST'])
def add_to_myBrews():
    session_user = g.user
    
    if session_user:
        # get recipe id
        myBrew_id = request.form.get('myBrew_id')
        # get database collections
        user = mongo.db.user
        brew_db = mongo.db.brew
        # get recipe to add to user collection myBrews
        myBrews_entry = brew_db.find_one({"_id": ObjectId(myBrew_id)})
        # get user
        session_user = g.user
        
        user_doc = mongo.db.user.find_one({'username':session_user})
        
        # enter recipe into user's recipe dashboard myBrews 
        user.update({'username': session_user},
            {"$addToSet":{"mybrews": {"_id": ObjectId(myBrew_id)}} }
        ) 
        return render_template('success.html', username=session_user)
        
    return render_template('login.html') 
    
@app.route('/insert-brew', methods=['GET','POST'])
def insert_brew():
    session_user = g.user
    
    if session_user:
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
       
        # add user input from profile form to the brew collection
        brews.insert_one({
                    "author": author_name,
                    "recipe_profile":{
                            "cat_name": category_name,
                            "recipe_name": recipe_name,
                            "recipe_description": recipe_description,
                            "style": style,
                            "level": level,
                            "flavour": flavour,
                            "region": region,
                            "method": method,
                            "properties": properties,
                            "free_from": freefrom, 
                            "recipe":{
                                "equip_list":[],
                                "ingredients_list":[],
                                "prep_method":[],
                            }
                        }
        })
        
        newBrew = brews.find_one({"author": author_name, "recipe_profile.recipe_name": recipe_name, "recipe_profile.recipe_description":recipe_description})
        
        return render_template('addBrewRecipe.html', username=session_user, newBrew=newBrew)
        
    return render_template('login.html') 
    
@app.route('/insert-brew-recipe', methods=['GET','POST'])
def insert_brew_recipe():
    # updates the newly created brew profile document with recipe data
    session_user = g.user
 
    if session_user:
        # get db
        brews = mongo.db.brew
        # get relevant id for newly created brew from hidden form input
        new_id = request.form['newBrew_id']
        
        # get form field submissions form add_recipe form
        equip_list = request.form['equip_list']
        ingredients_list = request.form.getlist('ingredients_list')
        prep_method = request.form.getlist('prep-method')
        
        # find & update new recipe doc with array values
        brews.update(
            {"_id": ObjectId(new_id)},
            {
                "$push":
                    {"recipe_profile.recipe.equip_list": {"$each": equip_list}}
            }
        )
        
        brews.update(
            {"_id": ObjectId(new_id)},
            {
                "$push":
                     {"recipe_profile.recipe.ingredients_list": {"$each": ingredients_list}}
            }
        )
        
        brews.update(
            {"_id": ObjectId(new_id)},
            {
                "$push":
                     {"recipe_profile.recipe.prep_method": {"$each": prep_method}}
            }
        )
        
        return render_template('success.html')
    return render_template('login.html') 
        
if __name__ == '__main__':
    app.secret_key = b'\xeb\xd3\x0c\x89P\xed.\x15~\xa6\xc6\xad;\x16\x8fH'
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)