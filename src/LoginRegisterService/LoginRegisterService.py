from flask import Flask
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort
from flask_cors import CORS

from model import UserSchema, UserLoginSchema, UserRegisterSchema, UserQuerySchema, UserDb, CouldNotConnectToDatabase, UserNotFound, UserAlreadyExists, IncorrectUsernameOrPassword, HealthSchema

app = Flask(__name__)
app.config['API_TITLE'] = 'LoginRegisterService'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

CORS(app)

api = Api(app)

blp = Blueprint("LoginRegisterService", __name__,
                url_prefix="", description="LoginRegisterService")

blp_health = Blueprint(
    "Health", __name__, url_prefix="/health", description="Health")

blp_metrics = Blueprint("Metrics", __name__,
                        url_prefix="/metrics", description="Metrics")


@blp_metrics.route("/")
class Metrics(MethodView):
    @blp.response(200)
    def get(self):
        return ({"application": {
            "db.writes": UserDb.writes, "db.reads": UserDb.reads, "db.cursors": UserDb.cursors}, "base": {}}, 200, {"Content-Type": "application/json"})


@blp_health.route("/live")
class HealthLive(MethodView):
    @blp.response(200, HealthSchema)
    @blp.response(503, HealthSchema)
    @blp.response(500)
    def get(self):
        try:
            db_check = {
                "name": "DataSourceHealthCheck",
                "state": "DOWN" if UserDb.has_error else "UP"
            }

            etcd_check = {
                "name": "EtcdHealthCheck",
                "state": "DOWN" if UserDb.has_etcd_error else "UP"
            }

            status = "DOWN" if any(
                [db_check["state"] == "DOWN", etcd_check["state"] == "DOWN"]) else "UP"
            code = 503 if status == "DOWN" else 200

            return ({
                "status": status,
                "checks": [db_check, etcd_check]
            }, code)
        except Exception as e:
            abort(500)


@blp_health.route("/ready")
class HealthReady(MethodView):
    @blp.response(200, HealthSchema)
    @blp.response(503, HealthSchema)
    @blp.response(500)
    def get(self):
        try:
            db_check = {
                "name": "DataSourceHealthCheck",
                "state": "DOWN" if UserDb.has_error else "UP"
            }

            etcd_check = {
                "name": "EtcdHealthCheck",
                "state": "DOWN" if UserDb.has_etcd_error else "UP"
            }

            status = "DOWN" if any(
                [db_check["state"] == "DOWN", etcd_check["state"] == "DOWN"]) else "UP"
            code = 503 if status == "DOWN" else 200

            return ({
                "status": status,
                "checks": [db_check, etcd_check]
            }, code)
        except Exception as e:
            abort(500)


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
api.register_blueprint(blp_health)
api.register_blueprint(blp_metrics)

if __name__ == '__main__':
    app.run(port=5002, host="0.0.0.0")
