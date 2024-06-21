import functools
from flask import Blueprint, request, jsonify, session
from flask_restx import Namespace, Resource, fields
from werkzeug.security import check_password_hash, generate_password_hash
from flaskblog.models import db
from flaskblog.models import User

auth = Blueprint('auth', __name__)
api = Namespace('auth', description='Authentication operations')

# User schema for input validation
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/register')
class Register(Resource):
    @api.expect(user_model)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        user = User.query.filter_by(username=username).first()
        if user is not None:
            return {'message': 'User already exists'}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201

@api.route('/login')
class Login(Resource):
    @api.expect(user_model)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            return {'message': 'Invalid credentials'}, 400

        session.clear()
        session['user_id'] = user.id
        return {'message': 'Login successful'}, 200

def login_required(func):
    @functools.wraps(func)
    def wrapped_view(**kwargs):
        if g.user is None:
            return {'error': 'Login required'}, 401
        return func(**kwargs)
    return wrapped_view


@api.route('/logout')
class Logout(Resource):
    # @login_required
    def post(self):
        session.clear()
        return {'message': 'Logout successful'}, 200







