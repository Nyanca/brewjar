import os
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'brewjar-app'
app.config['MONGO_URI'] = 'mongodb://admin:99Prism@ds225382.mlab.com:25382/brewjar_app'

mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'hello'
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)