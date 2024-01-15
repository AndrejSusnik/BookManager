from flask import Flask
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort
from flask_cors import CORS

from model import UserSchema, UserLoginSchema, UserRegisterSchema, UserQuerySchema, UserDb, CouldNotConnectToDatabase, UserNotFound, UserAlreadyExists, IncorrectUsernameOrPassword

app = Flask(__name__)
app.config['API_TITLE'] = 'LoginRegisterService'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

CORS(app)

api = Api(app)

blp = Blueprint("LoginRegisterService", __name__, url_prefix="/LoginRegisterService", description="LoginRegisterService")

@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserLoginSchema, location="json", as_kwargs=True)
    @blp.response(200, UserSchema)
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    @blp.response(401, description="Unauthorized")
    def post(self, **args):
        """Login"""
        try:
            user = UserDb.login(UserLoginSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            abort(503, message="Could not connect to database")
        except IncorrectUsernameOrPassword:
            abort(401, message="Incorrect username or password")
        except Exception as e:
            print(e)
            abort(404, message=str(e))
        
        return (user, 200)

@blp.route("/users")
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    @blp.response(404)
    def get(self):
        """Get all users"""
        try:
            users = UserDb.get_all()
        except CouldNotConnectToDatabase:
            abort(404, message="Could not connect to database")
        except Exception as e:
            abort(404, message=str(e))

        return (users, 200)

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    @blp.response(404)
    def get(self, user_id):
        """Get"""

        try:
            user = UserDb.get_by_id(user_id)
        except CouldNotConnectToDatabase:
            abort(404, message="Could not connect to database")
        except UserNotFound:
            abort(404, message="User not found")
        except Exception as e:
            abort(404, message=str(e))
        
        return (user, 200)
    
    @blp.arguments(UserRegisterSchema, location="json", as_kwargs=True)
    @blp.response(200, UserSchema)
    @blp.response(404)
    def post(self, _, **args):
        """Register"""
        try:
            user = UserDb.add(UserRegisterSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            abort(404, message="Could not connect to database")
        except UserAlreadyExists:
            abort(404, message="User already exists")
        except Exception as e:
            abort(404, message=str(e))
        
        return (user, 200)
            
    @blp.arguments(UserQuerySchema)
    @blp.response(200, UserSchema)
    @blp.response(404)
    def delete(self, user_id, **args):
        """Delete"""
        return "Not implemented", 501

    @blp.arguments(UserRegisterSchema)
    @blp.response(200, UserSchema)
    @blp.response(404)
    def put(self, user_id):
        """Update"""
        return "Not implemented", 501

api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(port=5002, host="0.0.0.0")
