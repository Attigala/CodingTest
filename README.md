# CodingTest
Running the project locally
clone the project
git clone https://github.com/Attigala/CodingTest.git

install the requirements
pip install -r requirements,txt

activate virtual environment
venv\Scripts\activate

create database
python manage.py migrate

insert data 
use the custom management command to insert data into the database by
python manage.py load_data
or insert data using the python shell

run the server
pythom namage.py runserver

use localhost:8000/accounts/login to login before accessing any urls
following are the conditions to access each url
localhost:8000/ : user must be logged in access accounts/login to login as a valid user
localhost:8000/team : the logged in user must be a valid coach who is assigned to a team
localhost:8000/teams : the logged in user must a valid user assigned to the user group "LeagueAdmin"
localhost:8000/highest: the logged in user must be a valid coach who is assigned to a team
