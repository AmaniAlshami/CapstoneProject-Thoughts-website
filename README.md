# CapstoneProject-Thoughts-website

## Introduction

Thoughts is a website to allow blogger share their thoughts, idea and content with others. This website has two users blogger and visitor. The blogger can write blog and comments but the visitor only can interact with blogger by writing comments. 
Note: this project is the last requirement to get Full-Stack Nanodegree by Udacity.



## Getting Started

In this project you need Python 3.7 or above and pip intsalled in your loacl machine.
[python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### 1. Backend 

**Install all required packages that are included in the requirements file.** 
```
cd backend
pip install -r requirements.txt
```
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

**Run the following commands to start the flask application**
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```



## API Reference

### Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

### Expected Errors and Messages


### Endpoints



Errors are returned as JSON objects in the following format:
```
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```
This API will return four error types when requests fail:

* 400: Bad Request
* 404: Resource Not Found
* 422: Not Processable
* 405: Method not allowed
* 403: Permission not found.
* 401: Invalid authorization header 


**Example of endpoints


**GET /blogs 

General:
Returns a list of blogs objects with success code that contian blogger id, blog id, content and title.
Sample: curl http://127.0.0.1:5000/blogs

```
{
  "blogs": [
    {
      "Bolgger_id": 1, 
      "content": "Hello this is a blog ", 
      "id": 2, 
      "title": "new blog"
    }
  ], 
  "success": true
}
```
**GET /bloggers 

General:
Returns a list of bloggers objects with success code that contian blogger id and name.
Sample: curl http://127.0.0.1:5000/bloggers

```
{
  "bolggers": [
    {
      "BloggerName": "Amani", 
      "id": 1
    }
  ], 
  "success": true
}
```

**GET '/blogs/${blog_id}'  

General:
Returns a blog objects with success code that contian blog id content, title and list of comments.
Sample: curl http://127.0.0.1:5000/blogs/2

```
{
  "comments": [], 
  "content": "Hello this is a blog ", 
  "id": 2, 
  "success": true, 
  "title": "new blog"
}
```


### Authentication

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:blogs`
   - `get:blogger`
   - `post:comment`
   - `post:blog`
   - `patch:blog`
   - `delete:blog`
6. Create new roles for:
   - Visitor
     - can `post:comment`
     - can `get:blogs`
     - can `get:blogger`
   - Blogger
     - can perform all actions
7. Test the endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Blogger role to one and Visitor role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./backend/Thoughts-website.postman_collection.json`
   - Right-clicking the collection folder for visitor and blogger, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
  

## Testing



## Deployment 


## Authors
AMANI ALSHAMI 
