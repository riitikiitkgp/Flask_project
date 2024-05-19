from flask import request
from flask_restful import Resource, reqparse
from models import db, User

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "company_name": user.company_name,
            "age": user.age,
            "city": user.city,
            "state": user.state,
            "zip": user.zip,
            "email": user.email,
            "web": user.web
        }, 200

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.age = data.get('age', user.age)
        db.session.commit()
        return {}, 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204

class UserListResource(Resource):

    def get(self):
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=5, type=int)
        search = request.args.get('search', default="")
        sort = request.args.get('sort', default="id")

        query = User.query
        if search:
            query = query.filter(
                User.first_name.ilike(f"%{search}%") |
                User.last_name.ilike(f"%{search}%")
            )

        if sort.startswith('-'):
            query = query.order_by(getattr(User, sort[1:]).desc())
        else:
            query = query.order_by(getattr(User, sort).asc())

        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        users = pagination.items

        return [{
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "company_name": user.company_name,
            "age": user.age,
            "city": user.city,
            "state": user.state,
            "zip": user.zip,
            "email": user.email,
            "web": user.web
        } for user in users], 200

    def post(self):
        data_list = request.get_json()  # Get the list of user data from the request

        # Iterate over each item in the list
        for data in data_list:
            user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                company_name=data['company_name'],
                age=data['age'],
                city=data['city'],
                state=data['state'],
                zip=data['zip'],
                email=data['email'],
                web=data['web']
            )
            db.session.add(user)

        db.session.commit()  # Commit changes after adding all users
        return {"message": "Users saved successfully"}, 201

