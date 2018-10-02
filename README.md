The GIF App
===========

This is a simple web application that runs on the Django web framework with a
sqlite database. It interacts with giphy.com's API to allow you to search for
gifs, save them to your account, and categorize them.

Running the application
-----------------------

The easiest way to run the application is to:
  - make sure you have python3 installed: https://www.python.org/downloads/
  - get an account on https://giphy.com and get an API key (used below)
  - git clone down the repo `git clone https://github.com/dpgoetz-temp/gapp.git`
  - `cd gapp`
  - create a python3 virtual environ `python3 -m venv venv`
  - activate the virtual environment `source venv/bin/activate`
  - install pkgs `pip install -r requirements.txt`
  - `cd gifapp`
  - build the development database: `python manage.py migrate`
  - you can run the unit tests using: `python manage.py test`
  - set the GIPHY_API_KEY in your environment: `export GIPHY_API_KEY=<your-api-key>`
  - to run a development server: `python manage.py runserver`

This will run a development server for the application. It will create a sqlite database
in the base directory of the application

Open http://127.0.0.1:8000/ in your browser. Create a user (please pay attention
to password specifications), log in with the user you just made, and follow the
instructions on the screen.

Description of Application
--------------------------

This application uses the Django web application framework. For ease of use it
uses a sqlite database as a backend but this could be easily switched using
Django's pluggable database features.

There are two installed apps and one middleware for this project.

The user setup (https://github.com/dpgoetz-temp/gapp/tree/master/gifapp/users)
uses Django's default user feature with the only real modification made on the
view side.

The main application is in:
https://github.com/dpgoetz-temp/gapp/tree/master/gifapp/gifs . The most
important parts being the models.py and the views.py . You can see the
endpoints available for the API in urls.py and the tests in tests.py. All the
views require a login and it uses the `request.searchForNewGifs` call (which is
installed via the middleware) to interact with the Giphy API.

The models.py contains the setup for the database. I just have 2 tables:
GifToUser and GifToUserCategory. When I started the project I had a separate
table for the gifs and the GifToUser was a many-to-many to the django user but
because I was just saving a single url to identify the gif I collapsed it into
the single table for simplicity. The same is true on the category side.

The html templating is in the gifapp/templates and gifapp/templates/gifs
directories and the javascript used to save the gif to your account is in
static/gifs/scripts.js .

I put the functionality to interact with the Giphy api in middleware:
gifs/middleware.py . When the server is stood up it sets up the client in its
__init__ function so it is only loaded once. It installs its search function
searchForNewGifs into each request as it is processed. This type of setup also
allows for other middlewares to be built for other Giphy-type APIs and be
easily plugged into the application. All they need to do is setup the
searchForNewGifs function on the request.
