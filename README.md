Brewjar is a web application for easy homebrewing recipe collections with user access. 

Logic is written in Python. The backend framework is Flask. The DBMS used is MongoDB. 

IMPROVEMENTS
The current login system represents my first attempt at building a log-in system. There is a clear issue with it in that it repeats itself by passing the session-user variable to each view function as an if..else statement instead of using @login-decorators and proper session handling. With more time, I would implement session handling with flask_login, flask-mongoengine and WTforms. 
