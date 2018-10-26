import os
import json
from bson import json_util
from pymongo import MongoClient
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
    
    # if request.method == ['POST']:
    #     hashed_password = bcrypt.generate_password_hash(request.form['password']).decode(utf-8)
    #     user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
    #     mongo.db.user.insert_one(user)
    
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
    return render_template('fullview.html', recipe_item=recipe_item)
    
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

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)