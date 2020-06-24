# Error Logging App 
This app allows users to track issues with laboratory instruments.  

Originally, errors were logged in a Google sheet, but the solution had a number of issues. Users were required to use personal Google accounts to gain access to the sheet. Additionally, users could accidentally over-write or delete records if not careful. Finally, querying all the records was cumbersome.  

The solution developed here allows users to upload errors to a central database with role-based access controls provided through Auth0. The users do not need to enmesh personal accounts with professional accounts, and the permissions administrated through Auth0 prevent users from over-writing or accidentally deleting records. At the same time, administrative rights allow users to safely curate the dataset, and queries can be reliably exectued through the web-based API. The security provided by Auth0 allows the data to be accessed both within and without the company's firewall, which has the additional advantage of allowing customers to upload their own data, providing a comprehensive picture of instrument performance.  

## Table of Contents

  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Authorization](#authorization)
      - [Create an Application](#create-an-application)
      - [Create an API](#create-an-api)
      - [Add permissions](#add-permissions)
      - [Add roles](#add-roles)
      - [Add environment variables](#add-environment-variables)
    - [Development](#development)
    - [Running Tests](#running-tests)
    - [Deployment](#deployment)
    - [API Functionality](#api-functionality)
      - [Authentication](#authentication)
      - [Error handling](#error-handling)
      - [Endpoints](#endpoints)
  - [Authors](#authors)
  - [License](#license)
  - [Notes for Udacity Reviewer](#notes-for-udacity-reviewer)

## Getting Started

### Prerequisites

The error-logging-app has the following major dependencies:
- Database: PostgreSQL
- Backend: Python 3.7
- Authorization: Auth0

The full list of python dependencies can be found in requirements.txt, including the following:
- Flask
- Flask-Migrate
- Flask-Script
- Flask-SQLAlchemy
- psycopg2
- pytest
- python-jose

### Installation

1. Clone the repository onto your local machine
2. Create a virtual environment in the project's top-level directory: ```python -m venv <name of virtual environment directory>```
3. Activate the virtual environment: ```source <virtual environment directory>/bin/activate```
4. Update pip: ```python -m pip install --upgrade pip```
5. Install required dependencies: ```python -m pip install -r requirements.txt```

## Usage

### Authorization

The error-logging-app utilizes Auth0 to provide authorization and role-based access control for the api endpoints. To set up Auth0, execute the following steps:  

#### Create an Application  
1. Create an [Auth0](www.auth0.com) account and log in
2. Applications > Create Application > Regular Web Application
3. Add a name for your app
4. Under "Allowed Callback URLs" add ```http://localhost:5000/```
5. If you will be hosting your app on a server, add the root url of the production app to "Allowed Callback URLs" as well
#### Create an API
1. APIs > Create API
2. Add a name for the API

#### Add permissions
1. Under RBAC Settings, make sure that "Enable RBAC" and "Add Permissions in the Access Token" are both enabled
2. Go to "Permissions" and add the following permissions: 
   - read:contacts
   - update:contacts
   - create:contacts
   - delete:contacts
   - read:instruments
   - update:instruments
   - create:instruments
   - delete:instruments
   - read:errors
   - update:errors
   - create:errors
   - delete:errors
#### Add roles
1. Under "Users & Roles", create an "administrator" role and assign all of the above permissions.
2. Create a "contact" role and assign the following permissions: 
   - read:contacts
   - read:instruments
   - read:errors
   - create:errors 
#### Add environment variables
The following environment variables need to be available for the app to integrate correctly with Auth0:
- AUTH0_DOMAIN: The Auth0 domain associated with your Auth0 account
- API_AUDIENCE: This is the name that you gave to the Auth0 API
- CLIENT_ID: Can be found in the "Settings" tab of the Auth0 app created above
- ALGORITHMS: Should be set to "RS256"

### Development
1. To run the app locally for development, first make sure that you have a postgresql server running on port 5432 and create a new database for the project
2. In addition to the [authorization environment variables](#add-environment-variables) listed above, set the following environment variables needed for the development version of the app:
   - APP_MODE: Set to "development"
   - DEV_REDIRECT_URI: Recommended to use http://127.0.0.1:5000/
   - DEV_DATABASE_URI: Associate the database created above, i.e., postgresql://<user>@localhost:5432/\<name of database>
   - FLASK_APP: Should point to the project/app directory, e.g., if in the top level directory of the project, then enter ```export FLASK_APP=app```
3. Start the app: ```flask run```
### Running Tests
1. To run tests locally, the [authorization environment variables](#add-environment-variables) from above are needed in addition to the following:
   - APP_MODE: Set to "test"
   - FLASK_APP: Should point to the project/app directory, e.g., if in the top level directory of the project, then enter ```export FLASK_APP=app```
   - ADMIN_TOKEN: This is a valid json web token (JWT) that is returned from Auth0 upon successfully signing in to the app with an admin account. To collect the token, start up the development server using the instructions above and then direct the browser to localhost:5000/login. Fill in the credentials for an admin user, and then locate the jwt in the redirect url.
   - CONTACT_TOKEN: This is a valid JWT returned from Auth0 after signing into the app with a restricted "Contact" account. Use the instructions for collecting the admin JWT, only use a contact account. 
   - EXPIRED_TOKEN: This is a JWT that has expired. It is used to ensure that the authorization code in the app can correctly prevent an expired JWT from accessing secure endpoints.
2. A local postgresql database server needs to be running on port 5432
3. Run ```test.sh```
   - The script will set up a temporary postgresql database using the tests/setup_test_db.sql commands
   - Next, the script invokes pytest to run the test suite in tests/test_app.py
   - Finally, the script tears down the temporary database using the tests/teardown_test_db.sql commands

### Deployment
Deployment requires the [authorization environment variables](#add-environment-variables) listed above in addition to the following:
   - APP_MODE: Set to "production"
   - DATABASE_URL: The URI for the production database
   - REDIRECT_URI: After logging in, a user will be redirected to this website

### API Functionality

#### Authentication
API requests requre an "Authorization" header with the value "Bearer \<JWT>", where JWT is a json web token provided and validated by Auth0. Role-based access control is provided for the following two roles and associated permissions:
|Role         |Permissions       |
|-------------|------------------|
|Administrator|read:contacts     |
|             |create:contacts   |
|             |update:contacts   |
|             |delete:contacts   |
|             |read:instruments  |
|             |create:instruments|
|             |update:instruments|
|             |delete:instruments|
|             |read:errors       |
|             |create:errors     |
|             |update:errors     |
|             |delete:errors     |
|Contact      |read:contacts     |
|             |read:instruments  |
|             |read:errors       |
|             |create:errors     |

#### Error handling
Errors are returned as JSON objects in the follwing format:
```javascript
{
  "message": "error message", // e.g., Authorization header missing
  "status_code": 4xx          // e.g., 401
}
```
The following errors are possible:  
|Code       |Type               |
|-----------|-------------------|
|400        |Bad request        |
|401        |Authorization error|
|403        |Access forbidden   |
|404        |Resource not found |
|500        |Server error       |

#### Endpoints

GET /contacts
- General: Returns users of the error-logging-app
- Permissions required: "read:contacts"
- Example: ```curl -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/contacts```
```javascript
{
  "contacts": [
     {
        "department": "department1",
        "first_name": "contact",
        "id": 1,
        "last_name": "1"
     },
     {
        "department": "department2",
        "first_name": "contact",
        "id": 2,
        "last_name": "2"
     }
  ],
  "page": 1
}
```

GET /contacts/\<contact id>
- General: Returns data for the contact with the given contact id (an integer)
- Permissions required: "read:contacts"
- Example: ```curl -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/contacts/1```
```javascript
{
  "department": "department1",
  "first_name": "contact",
  "id": 1,
  "last_name": "1"
}
```

POST /contacts
- General: Adds a new user ("contact") to the error-logging-app
- Permissions required: "create:contacts"
- Example: ```curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"first_name": "contact", "last_name": "3", "department": "department3"}' https://error-logging-app.herokuapp.com/contact```
```javascript
{
  "department": "department3",
  "first_name": "contact",
  "id": 3,
  "last_name": "3"
}
```

PATCH /contacts/\<contact id>
- General: Updates the indicated contact record
- Permissions required: "update:contacts"
- Example: ```curl -X PATCH -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"department": "department1"}' https://error-logging-app.herokuapp.com/contacts/3```
```javascript
{
  "department": "department1",
  "first_name": "contact",
  "id": 3,
  "last_name": "3"
}
```

DELETE /contacts/\<contact id>
- General: Deletes the indicated contact record
- Permissions required: "delete:contacts"
- Example: ```curl -X DELETE -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/contacts/3```
```javascript
{
  "department": "department1",
  "first_name": "contact",
  "id": 3,
  "last_name": "3"
}
```

GET /instruments
- General: Returns all instruments monitored with the error-logging-app
- Permissions required: "read:instruments"
- Example: ```curl -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/instruments```
```javascript
{
  "instruments": [
    {
      "id": 1,
      "ip_address": "0.0.0.1",
      "serial_number": "SN001"
    },
    {
      "id": 2,
      "ip_address": "0.0.0.2",
      "serial_number": "SN002"
    }
  ],
  "page": 1
}
```

GET /instruments/\<instrument id>
- General: Return the information for the instrument with the given instrument id
- Permissions required: "read:instruments"
- Example: ```curl -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/instruments/1```
```javascript
{
  "id": 1,
  "ip_address": "0.0.0.1",
  "serial_number": "SN001"
}
```

POST /instruments
- General: Add an instrument to be monitored
- Permissions required: "create:instruments"
- Example: ```curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"serial_number": "SN003", "ip_address": "0.0.0.3"}' https://error-logging-app.herokuapp.com/instruments``` 
```javascript
{
  "id": 3,
  "ip_address": "0.0.0.3",
  "serial_number": "SN003"
}
```

PATCH /instruments/\<instrument id>
- General: Update the information for a particular instrument
- Permissions required: "update:instruments"
- Example: ```curl -X PATCH -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"ip_address": "1.0.0.3"}' https://error-logging-app.herokuapp.com/instruments/3```
```javascript
{
  "id": 3,
  "ip_address": "1.0.0.3",
  "serial_number": "SN003"
}
```

DELETE /instruments/\<instrument id>
- General: Delete an instrument from the app
- Permissions required: "delete:instruments"
- Example: ```curl -X DELETE -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/instruments/3```
```javascript
{
  "id": 3,
  "ip_address": "1.0.0.3",
  "serial_number": "SN003"
}
```

GET /errors
- General: List all the errors logged in the app
- Permissions required: "read:errors"
- Example: ```curl -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/errors```
```javascript
{
  "errors": [
    {
      "contact": {
        "department": "department1",
        "first_name": "contact",
        "id": 1,
        "last_name": "1"
      },
      "date": "Sun, 31 May 2020 16:42:21 GMT",
      "description": "broken",
      "id": 1,
      "instrument": {
        "id": 1,
        "ip_address": "0.0.0.1",
        "serial_number": "SN001"
      },
      "is_resolved": false
    }
  ],
  "page": 1
}
```

GET /errors/\<error id>
- General: Fetch the infromation from a particular error
- Permissions required: "read:errors"
- Example: ```curl -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/errors/1```
```javascript
{
  "contact": {
    "department": "department1",
    "first_name": "contact",
    "id": 1,
    "last_name": "1"
  },
  "date": "Sun, 31 May 2020 16:42:21 GMT",
  "description": "broken",
  "id": 1,
  "instrument": {
    "id": 1,
    "ip_address": "0.0.0.1",
    "serial_number": "SN001"
  },
  "is_resolved": false
}
```

POST /errors
- General: Log a new instrument error
- Permissions required: "create:errors"
- Example: ```curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"contact": 2, "instrument": 2, "description": "small explosion"}' https://error-logging-app.herokuapp.com/errors```
```javascript
{
  "contact": {
    "department": "department2",
    "first_name": "contact",
    "id": 2,
    "last_name": "2"
  },
  "date": "Sun, 21 Jun 2020 23:10:26 GMT",
  "description": "small explosion",
  "id": 2,
  "instrument": {
    "id": 2,
    "ip_address": "0.0.0.2",
    "serial_number": "SN002"
  },
  "is_resolved": false
}
```

PATCH /errors/\<error id>
- General: Change information logged with a particular instrument error
- Permissions required: "update:errors"
- Example: ```curl -X PATCH -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"is_resolved": true}' https://error-logging-app.herokuapp.com/errors/2```
```javascript
{
  "contact": {
    "department": "department2",
    "first_name": "contact",
    "id": 2,
    "last_name": "2"
  },
  "date": "Sun, 21 Jun 2020 23:10:26 GMT",
  "description": "small explosion",
  "id": 2,
  "instrument": {
    "id": 2,
    "ip_address": "0.0.0.2",
    "serial_number": "SN002"
  },
  "is_resolved": true
}
```

DELETE /errors/\<error id>
- General: Delete an error
- Permissions required: "delete:errors"
- Example: ```curl -X DELETE -H "Authorization: Bearer <JWT>" https://error-logging-app.herokuapp.com/errors/2```
```javascript
{
  "contact": {
    "department": "department2",
    "first_name": "contact",
    "id": 2,
    "last_name": "2"
  },
  "date": "Sun, 21 Jun 2020 23:10:26 GMT",
  "description": "small explosion",
  "id": 2,
  "instrument": {
    "id": 2,
    "ip_address": "0.0.0.2",
    "serial_number": "SN002"
  },
  "is_resolved": true
}
```

## Authors
Joshua Tice

## License
MIT License

## Notes for Udacity Reviewer

To set up the project for evaluation, the following steps may be followed.
- Clone the repository: ```git clone https://github.com/joshtice/fullstack_final_project.git```
- Create a virtual environment: ```python -m venv venv```
- Activate the virtual environment: ```source venv/bin/activate```
- Upgrade pip: ```python -m pip install --upgrade pip```
- Install dependencies: ```python -m pip install -r requirements.txt```
- Ensure that postgresql is [installed](https://www.postgresql.org/download/) and [running](https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html)
- Create a database for the API: ```createdb <database name>```
- Open setup.sh and enter the database URI on the top line (you'll need to adjust 'username' and 'database name'): ```export DEV_DATABASE_URI='postgresql://<username>@localhost:5432/<database name>```
- Load the required environment variables in setup.sh: ```source setup.sh```
- If you would like to interact with the development version of the app, then enter ```flask run``` and query the API through http://localhost:5000 with the provided authorization tokens, *e.g.*
  - Admin token: ```curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:5000/errors```
  - Contact token: ```curl -H "Authorization: Bearer $CONTACT_TOKEN http://localhost:5000/contacts```
- If you would like to run the project's tests, then be sure that your local postgresql server is running and run ```./test.sh```
