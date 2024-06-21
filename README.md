# Flask Blog Project
A simple blog application built using Flask and Flask-Restx.<br> This project demonstrates basic CRUD operations for blog posts and includes user authentication features.

## Features
- User registration
- User login and logout
- Create, view, and delete blog posts
  
## Requirements
- Flask
- Flask-Restx
- Flask-SQLAlchemy
- pytest

## Installation

### Prerequisites
- Python 3.10 or higher
- Virtual environment tool

**Clone the repository:**
```bash
git clone https://github.com/bhatisakshi/flask-blog.git
cd flask-blog
```

**Create and activate a virtual environment:**
```bash
virtualenv venv
source venv/bin/activate 
```
**Install the dependencies:**
```bash
pip install -r requirements.txt
```

## Project Setup

1. Initialize the database:
```bash
flask init-db
```
2. Set up os environment variable:(in the root directory of .env file in your project or in the command prompt):
```bash
export FLASK_APP=flaskblog
```
3.  Run the application:
```bash
flask run
```
The application will be available at http://127.0.0.1:5000/

## Endpoints

### Authentication Endpoints
- POST /auth/register: Register a new user
- POST /auth/login: Log in a user
- POST /auth/logout: Log out a user

### Blog Endpoints
- GET /blog/posts: List all posts
- POST /blog/posts: Create a new post
- GET /blog/posts/int:id: Fetch a single post by id
- PUT /blog/posts/int:id: Update a post by id
- DELETE /blog/posts/int:id: Delete a post by id

## Testing
To run the tests, use pytest:
```bash
pytest
```
