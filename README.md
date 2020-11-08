# Udacity Capstone Casting Agency Python/Heroku Application

## Description

This is the last project of the Udacity-Full-Stack-Nanodegree Course. It covers following technical topics in 1 application:

- Database modeling with postgres & sqlalchemy (see models.py)
- API to performance CRUD Operations on database with Flask (see app.py)
- Automated testing with Unittest (see test_app)
- Authorization & Role based Authentication with Auth0 (see auth.py)
- Deployment on Heroku

# Getting Started
The goal of this project is to run a Flask application into a Heroku envorinment. You will need some knowledge of the following:
* Python
* PostgreSQL
* AUTH0
* JWT
* Heroku
* HTML
* Git

# Setup Auth0

### 1) Create a new Auth0 Account
* Select a unique tenant domain
* Create a new, single page web application

### 2) Create a new API
* Enable RBAC
* Enable Add Permissions in the Access Token

### 3) Create new API permissions:
        -get:actors
        -get:movies
        -post:actors
        -post:movies
        -patch:actors
        -patch:movies
        -delete:actors
        -delete:movies

### 4) Create new roles for:

#### Casting-Assistant:

        permissions:
            -get:actors
            -get:movies
            
 #### executive-producer:
        permissions:
            -delete:movies
            -patch:movies
            -post:movies
            
#### casting-director:
        permissions:
            -delete:actors
            -patch:actors
            -patch:movies
            -post:actors

### 5) How to obtain JWT Tokens:

A. Open the application: https://127.0.0.1/login
Enter the following Information to generate the correct AUTH0 URI to generate the login page and generate a JWT token for either the assistant, producer or director permissions.
- Domain: The AUTH0 you create in step 1
- Audience: The audience you created from Step 2
- client_id: The ATHO clien id from step 1
- redirect_uri: The url you provided as the Allowed Callback URLs in AUTH0

The script will generate the appropriate URL to login into the AUTH0 interface and generate a JWT token. The following is an example of the generated URL:

https://{YOUR_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={AUTHO_CLIENT_ID}&redirect_uri={CALLBACK_URL}

### Postman Collections
Please see the two .json files which include the collections for the localhost and the remove Heroku application to run Postman Runner test. Add the appropriate tokens permissions for each profile. Also, be sure to update the FULL URL of the Heroku app.


## Project Dependencies, local development, Hosting Instruction, Environmental Variables


### Environmental Variables:

Install dotenv
```pip install dotenv```

Set settings variables to the .env file according to your AUTH0 and Heroku account details.

* AUTH0_API_AUDIENCE=""
* AUTH0_APP_CLIENT_ID=""
* AUTH0_SIGNING_ALGORITHM = "RS256"
* AUTH0_ALLOWED_CALLBACK_URL="https://127.0.0.1:5000/token"
* ASSISTANT_TOKEN = ""
* PRODUCER_TOKEN = ""
* DIRECTOR_TOKEN = ""
* LOCALSERVER="https://127.0.0.1:5000" 
* LOCALSERVER_PORT="5000" 
* DATABASE_URL = "postgresql://<USER>:<PASSWORD>@localhost:5432/<DATABASE_NAME>"
* HORUKO_APP_NAME="castingapp-20201107-1836"
* HORUKO_DATABASE_URL=""
* HORUKOHOST="https://YOUR_APP_NAME.herokuapp.com"
* AUTH0_ALLOWED_CALLBACK_URL_HEROKU="https://<YOUR_APP_NAME>.herokuapp.com/token"


## Dependencies:
- This script was built using Python 3.8.5 
- All the related dependencies are in the requirements.txt


## Create a virtualenv and install dependencies

### 1) Install Virtualenv  

```python -m pip install --user virtualenv```

### 2) Create Virtualenv in local project

```virtualenv -p /usr/bin/python3 env```

### 3) Install needed dependencies:

```pip install -r requirements.txt```

## How To Run App:

You must run this application in development server using https secured protocol.

```flask run --reload --port 5000 --cert=adhoc```

How to run tests:

```python3 test_app.py```

Example Output:

``` 
......................
    ----------------------------------------------------------------------
    Ran 22 tests in 5.767s

    OK
```  


# API ENDPOINTS AND EXAMPLE RESPONSE

### Actors Endpoints

#### List Actors:
Query paginated actors.
```curl -X GET https://127.0.0.1:5000/actors```

#### Create Actors:
Insert new actor into database.
```curl -X POST https://127.0.0.1:5000/actors```


#### Update Actors:
Edit an existing Actor:
```curl -X PATCH https://127.0.0.1:5000/actors/1 ```

#### Delete Actors:
Delete an existing Actor:   
```curl -X DELETE https://127.0.0.1:5000/actors/1```

### Movies Endpoints

#### List Movies:
List paginated movies:
```curl -X GET https://127.0.0.1:5000/movies```


#### Create Movies:
Insert new Movie into database:
```url -X POST https://127.0.0.1:5000/movies```

#### Edit Movies:
Edit an existing Movie:
```curl -X PATCH https://127.0.0.1:5000/movie```

#### Delete Movies:
Deleting a movie
```curl -X DELETE https://127.0.0.1:5000/```

## References:
 * https://stackoverflow.com/
 * https://www.python.org/
 * https://auth0.com/
 * https://www.heroku.com/
 * https://jwt.io/

