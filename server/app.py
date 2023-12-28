#!/usr/bin/env python3

from flask import request, session, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        if 'username' not in json:
            return {'error': 'Missing username in request data'}, 400


        user = User(
            username=json['username'],
            password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if user_id:
            user = User.query.get(user_id)
            if user:
                return jsonify(user.to_dict()),200
            else:
                return {'message': 'User not found'}, 404
        return {}, 204

class Login(Resource):
    def post(self):
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return {'message': 'Both username and password are required'},

        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['user_id']= user.id

            return jsonify(user.to_dict())
        return {'message': 'Invalid credentials'}, 401

class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id', None)
            return {}, 204
        else:
            return {'message': 'User is not logged in'}, 401

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)