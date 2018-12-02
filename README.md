# Brewjar Online Recipe Store

### Intro Summary
This project has been developed as part of CI Dublin's coding bootcamp for software developers following modules in HTML, CSS, User Centric Frontend Dev, Javascript Fundamentals, Interactive Frontend Dev, Python Fundamentals, Practical Python and Data Centric Dev. The brief was to create an online recipe store, and so I created Brewjar. 

Brewjar is a web application for easy homebrewing recipe collections with user access. Homebrewing is a becoming more popular these days with cheap equipment available alongside plenty of information. From medicinal kombucha drinks to home brew beers and wines, Brewjar should be a place where users can easily access a plethora of interesting recipes uploaded by the community. 

While researching other similar applications I came upon a few sites that took subscription payments for this type of service such as https://www.brewersfriend.com/homebrew/recipe/calculator. This is a great resource for detailed information about brewing beer, and it gave me lots of ideas. However, the interface is intimidating to new-comers to brewing, full of calculative tools and complicated specs. Brewjar caters for new comers and advanced brewers alike through the application of a simple interface. It also encompasses a range of alcoholic and non-alocoholic brews which seems to be an original design factor.

## UX

As aforementioned, the simplcity of Brewjar's interface is an important aspect of the intended user experience. Brewjar has been designed as an explicitly unintimidating and highly accesible brewing 
environment. All functionality should be intuitive, and the user should be guided throughout the site without any confusion or frustration.

Traversing the site should be quick and easy. Here are some user stories I wrote in the planning phase that assisted with the conception of the Brewjar interface: 

    1) I'm tired of buying expensive beer and wine. I want to make my own, but there's so much information out there it makes my head hurt. I need a single place that gives me clear and simple direction on how to do it. 
    2) I'm a diy sort of girl, so I tried some online brewing sites to create my own brews, but I found the layout confusing so I gave up. I want to try again though!
    3) I work all day everyday, so I'm always tired. I'd like to be able to make my own food, drinks etc etc but I don't have the energy to wade through information. It would be great to have a place that caters for my lack of energy in this area, somewhere that does the work for me and presents it back it a simple way!
    4) I'm always making my own everything! I love to find a great resource that is easy to use and has lots of new ideas for me to exeperiment with.
    5) As a Brewjar member, I want to access tasty, healthy and easy recipes for different beverages.
    6) As a Brewjar member, I want to share my recipes with other users and promote my homebrewing social media pages and blog
    7) As a Brewjar member with little experience in brewing or using computers, I want both the web application and the recipes to be very easy to access and to understand
    8) As a Brewjar member, and an advancing brewer I want to find new and innovative recipes and techniques for home-brewing
    9) As a novice brewer, I want to join a community to learn new things from

The wireframe created for this project can be found here: https://marvelapp.com/explore/3331449/brewjar 
(**Note: you can access beyond the login pages by clicking on the create account / sign in buttons. )

## Data Schema    
I'm using MongoDB as database store and therefore the data schema for this project is noSQL. This is favourable as I can change the schema throughout the progression of the application. However, I also explored relational structures which can be seen as I studied the section blocks of data to include in /wireframe&planning/Brewjar mySQL - Sheet1.pdf/. The actual shape of my data currently is more relational than non-relational because that seems to be the way my head works. All the same, I see the value in non-relational application, and I quite like that my structure is set and yet I have the freedom to change the format of any document within the collection simultaneously. 

To begin I found a resource which suggested the ideal data structure is all contained within a single document, and so I deeply nested all of my data after deciding upon included fields which can be seen at /wireframe&planning/data.json/. However, this data was near impossible to access and iterate through which cost a lot of time failing to use mongoDB queries. I therefore split the data in separate documents while maintaining the structure, and finally I was up and running. 

## Tech used 
Logic is written in Python 3, a language I love to use largely because of it's visual attributes https://www.python.org/

Materialize was used as a frontend framework and provided easy form styling, navigation, sticky footer and accordion selectors. https://materializecss.com/

Fonts came from google fonts which are easily imported to any css or html document https://fonts.google.com/

The backend framework is the micro framework Flask. http://flask.pocoo.org/

The DBMS used is MongoDB, which I found highly intuitive and well documented. https://www.mongodb.com/

HTML5 is used in conjunction with Jinja http://jinja.pocoo.org/ to create dynamic templates and to prevent repetition of components such as head links, navs and footer. 

Sass is used for styling. It's an incredible resource that made the styling of this application a real pleasure. https://sass-lang.com/

## Features 
### existing features

1) User login system implemented at a basic level
2) Users can log in to their own dashboard and choose from 3 options 1) Browse 2) Create a Brew 3) Visit MyBrews
    i) Option 1 brings the users to a filter form where they can select from a number of filter options to refine the database results
    ii) Option 2 allows the user to input a new recipe into the database via two forms, a recipe form and a recipe profile form. These forms correspond directly to the data schema. 
    iii) Option 3 brings the users to their dashboard where they can view recipes which they have saved to myBrews from the online recipe store.
4) Brewjar extends basic CRUD operations

## improvements / issues
1) The current login system represents my first attempt at building a log-in system. There is a clear issue with it in that it repeats itself by passing the session-user variable to each view function as an if..else statement instead of using @login-decorators and proper session handling. With more time, I would implement session handling with flask_login, flask-mongoengine and WTforms.

2) The filter: The current filter is functioning at a very basic level. It will return any document that has one of the selected queries. I would implement a better filter that returns only documents with all of the specified queries. Further, if there are no results it returns blank. I attempted adding an if..else statement where else read 'No recipes match your search. Please try again'. However, this statement would be printed numerous times on the page, seemingly for each iteration that returned blank. This is a bug to be worked on. 

Further all fields must be filled out within the filter form. I would make it so that fields can be left blank for real world functionality, as this is ultimately standard behaviour expected by the user. 

3) The form creation functionality must be improved upon. The form for recipe profile creation works well. The recipe document itself is then nested within the recipe profile doc. Further, this nested recipe doc contains nested arrays. It has proved difficult to append data to these nested arrays as intended. For example: 

Form data can be added to the the nested array 'ingedients_list' like so: 

     brews.update(
            {"_id": ObjectId(new_id)},
            {
                "$push":
                     {"recipe_profile.recipe.ingredients_list": {"$each": ingredients_list}}
            }
        )
        
    ingredients_list = ['sugar', 'water', 'hops']
        
However, the result of this creates a single string from all of the form data within the DB collection doc. This is not useful for iteration: 

    ingredients_list = ["/'sugar'/'water'/'hops'"]

I have tried using $split to separate the values at the ',' interval specified as the form input format. However, while I have found that $out can transfer data from a pipeline to a collection, I have not yet discovered a method to update a single document with the new aggregated value. 

## TESTING
### Manual Testing: 
This application has been tested manually. Here are some example scenarios: 

    1) Test that create account and login work as expected: 
        i) Create account 'admin'
        ii) Login with account 'admin'
        iii) Click through each of the pages to see that username 'admin' is being displayed on every page in the top right hand corner. 
    2) Test that form input for create a brew works as expected: 
        i) input data to form fields
        ii) ensure submission of first form redirects to second form
        iii) ensure submission of the second form redirects to the success page, letting me know that the data has been appended to the DB 
    *this test was very useful with debug mode =True, informing me of errors or bugs which were disrupting functionality
    3) Test that filter displays accurate results:
        i) input filter form data
        ii) compare results with DB collection documents
    *this test made me aware that the filter form must be filled out in full because the view function requests data from each field, so empty fields raise a KeyError. 

### Unittest    
Testing has been carried out using unittest. 

### THANKS
Throughout the development process I found the following tutorials by DiscoverFlask very userful: https://github.com/realpython/discover-flask

