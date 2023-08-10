import datetime

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from extendsions import db
from models import User, Role

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')
user_parser.add_argument('roles', type=str, action='append', help='Roles should be a list of strings')


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"code": 404, "data": None, "message": "User not found"}, 404
        return {
            "code": 200,
            "data": {
                "id": user.id,
                "username": user.username,
                "roles": [role.role_name for role in user.roles]
            },
            "message": "Success"
        }

    def post(self):
        args = user_parser.parse_args(strict=True)

        username = args['username']
        password = args['password']
        roles = args['roles']

        user = User(username=username, password=password)
        if roles:
            for role_name in roles:
                role = Role.query.filter_by(role_name=role_name).first()
                if role:
                    user.roles.append(role)

        db.session.add(user)
        db.session.commit()
        return {"code": 200, "data": {"id": user.id}, "message": "User created successfully"}, 200

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"code": 404, "data": None, "message": "User not found"}, 404

        args = user_parser.parse_args(strict=True)

        username = args['username']
        password = args['password']
        roles = args['roles']

        user.username = username
        user.password = password

        # Clear existing roles and add new roles if provided
        user.roles.clear()
        if roles:
            for role_name in roles:
                role = Role.query.filter_by(role_name=role_name).first()
                if role:
                    user.roles.append(role)

        db.session.commit()
        return {"code": 200, "data": {"id": user.id}, "message": "User updated successfully"}, 200

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"code": 404, "data": None, "message": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"code": 200, "data": None, "message": "User deleted successfully"}, 200


# Request parser for user login
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Username is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')


class UserMethods(Resource):
    @jwt_required()
    def get(self, method):
        if 'info' == method:
            return self.info()

    def post(self, method):
        if 'login' == method:
            return self.login()

    def login(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.password == password:
            return {"code": 401, 'data': None, "message": "Invalid credentials"}, 401

        # Add your login logic here, for example, setting up a session or generating a token
        token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(seconds=3600), fresh=True,
                                    additional_claims={'role': 'admin', 'is_verified': True})

        return {"code": 200, 'data': {"token": token}, "message": "Login successful"}, 200

    def info(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return {
            "code": 200,
            "data": {
                "username": user.username,
                "roles": [role.role_name for role in user.roles]
            },
            "message": "Success"
        }
