<h1>Airport API Service ✈️🌎📆</h1>

<h3>Welcome to the global airport flight tracking system:</h3>
<ul>
   <li>The Airport API Service, built with Django, efficiently manages and tracks flights from worldwide airports.</li>
   <li>This system facilitates efficient coordination and information management.</li>
   <li>The system's structured features allow users to manage various aspects of the aviation ecosystem.</li>
</ul>

### 🏞 Airport API Endpoints:
![Airport API endpoints](images/airport%20api%20endpoints.png)

## Project Features:
- **Authentication:** Users are authenticated with JWTs issued at login for secure access.
- **Admin Panel:** Admins can manage data efficiently by adding, editing, and deleting entries.
- **Documentation:** API documentation is available via Swagger UI.
- **Airplane Management:** Define and categorize different types of airplanes, capturing details like capacity.
- **Crew Management:** Manage crew members, including their first and last names.
- **Location Handling:** Record country and city information, linking airports to nearby big cities.
- **Airport Details:** Store detailed airport data, including names, cities, and images.
- **Route Definition:** Define routes between airports to organize flight connections.
- **Flight Tracking:** Monitor flights with route, airplane, departure, arrival times, and crew details.
- **Order and Ticket System:** Manage user orders and tickets with flight, row, and seat details.

### 🏞 Swagger Documentation:
![Swagger documentation](images/swagger%20documentation.png)

## Installation and Usage:
<ul>
    <li><strong>Install Python 3.10.</strong></li>
    <li><strong>Install PostgreSQL and create db.</strong></li>
    <li><strong>Install Docker.</strong></li>
    <li><strong>Clone the repository.</strong></li>
    <li><strong>Set up environment variables using ".env.sample" as a guide.</strong></li>
    <li><strong>Run the application.</strong></li>
    <li><strong>Feel free to explore and contribute!</strong></li>
</ul>

```shell
git clone https://github.com/ArtemLeo/airport-api-service.git

(for Windows)
python -m venv venv
source venv/Scripts/activate

(for Mac/Linux)
python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

set DJANGO_SECRET_KEY=<your secret key>
set DJANGO_DEBUG=<your debug value>
set DJANGO_ALLOWED_HOSTS=<your allowed hosts>
set POSTGRES_HOST=<your Postgres host>
set POSTGRES_DB=<your Postgres database>
set POSTGRES_USER=<your Postgres user>
set POSTGRES_PASSWORD=<your Postgres password>

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Run with Docker:
docker-compose build
docker-compose up
```

### 🏞 DB Structure:
![DB structure](images/db%20structure.png)

## Stages of Project Creation:

<ul>
    <li><strong>Initialization of the Project:</strong></li>
    - Set up the initial Django project structure.<br> 
    - Configure project settings such as database connection and Django applications.
    <li><strong>Environment Setup:</strong></li>
    - Add the requirements.txt file and environment variables (SECRET_KEY, PostgreSQL settings) in ".env-sample".<br>
    - Switch to the PostgreSQL database and change TIME_ZONE.
    <li><strong>App Structure Organization:</strong></li>
    - Create empty User and Airport apps.<br>
    - Add these apps to INSTALLED_APPS.
    <li><strong>Model Creation:</strong></li>
    - Implement User, and UserManager models without the username field.<br>
    - Create Country, City, Airport, Route, Flight, Order, Ticket, AirplaneType, Airplane, and Crew models.<br>
    - Add verbose names and unique constraints.
    <li><strong>Migrations and Admin Setup:</strong></li>
    - Create initial migrations and register models in the admin site.<br>
    - Implement UserAdmin without the username field.
    <li><strong>Authentication and Authorization Setup:</strong></li>
    - Add REST framework and JWTAuthentication.<br>
    - Configure permission and throttle classes.<br>
    - Add settings for drf_spectacular.
    <li><strong>ViewSets and Serializers Creation:</strong></li>
    - Implement ViewSets and serializers for AirplaneType, Airplane, Airport, Route, Flight, Order, and Ticket.<br>
    - Add filters and configurations for serializers.
    <li><strong>Testing:</strong></li>
    - Implement tests for admin and unauthenticated requests.<br>
    - Create tests for CRUD operations and data filtering.
    <li><strong>Docker:</strong></li>
    - Create Dockerfile, ".dockerignore", and docker-compose.yml.<br>
    <li><strong>Documentation:</strong></li>
    - Update README.md with the project description.<br>
    - Add images and other materials in the images directory.<br>
    - Update database structure and project description.
    <li><strong>Additional Changes and Fixes:</strong></li>
    - Fix and improve save methods in models.<br>
    - Update ".gitignore" to include new directories.<br>
    - Refactor code using "black" and "flake8".
</ul>

### 🏞 Admin Page:
![Admin page](images/admin%20page.png)

## Getting Access:
- create a user via: **/api/user/register**
- get access token via: **/api/user/token**
