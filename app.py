import logging
from flask import Flask
from flask_restful import Api
from config import Config
from models import db
from resources import UserResource, UserListResource


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
