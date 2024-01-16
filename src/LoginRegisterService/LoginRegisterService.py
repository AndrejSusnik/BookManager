from flask import Flask
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort
from flask_cors import CORS
from etcd import Client as EtcdClient
import logging

from config_managment import CustomConfigManager, EtcdConfig

from model import EtcdDemoSchema, EtcdQuerySchema, ConfigQuerySchema, ConfigDemoSchema, UserSchema, UserLoginSchema, UserRegisterSchema, UserQuerySchema, UserDb, CouldNotConnectToDatabase, UserNotFound, UserAlreadyExists, IncorrectUsernameOrPassword, HealthSchema

from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.handler import LogstashFormatter

tmp = CustomConfigManager()
logger = logging.getLogger("logstash")
logger.setLevel(logging.DEBUG)

# Create the handler
handler = AsynchronousLogstashHandler(
    host=tmp.get("LOGIT_HOST", default="localhost"),
    port=19927,
    ssl_enable=True,
    ssl_verify=False,
    transport='logstash_async.transport.BeatsTransport',
    database_path='')
# Here you can specify additional formatting on your log record/message
formatter = LogstashFormatter()
handler.setFormatter(formatter)

# Assign handler to the logger
logger.addHandler(handler)

logger.debug("Configuring etcd with host: %s and port: %s", tmp.get("ETCD_HOST", default="localhost"), tmp.get("ETCD_PORT", default=2379))
conf = EtcdConfig(port=int(tmp.get("ETCD_PORT", default=2379)),
                  host=tmp.get("ETCD_HOST", default="localhost"))
config = CustomConfigManager(useEtcd=True, ectd_config=conf)

app = Flask(__name__)
app.config['API_TITLE'] = 'LoginRegisterService'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_JSON_PATH'] = 'openapi.json'

CORS(app)

api = Api(app)

blp = Blueprint("LoginRegisterService", __name__,
                url_prefix="", description="LoginRegisterService")

blp_health = Blueprint(
    "Health", __name__, url_prefix="/health", description="Health")

blp_metrics = Blueprint("Metrics", __name__,
                        url_prefix="/metrics", description="Metrics")

blp_etcd_demo = Blueprint("EtcdDemo", __name__, url_prefix="/etcd_demo")


@blp_etcd_demo.route("/etcd")
class EtcdDemo(MethodView):
    @blp_etcd_demo.response(200, EtcdDemoSchema)
    @blp_etcd_demo.arguments(EtcdQuerySchema, location="query")
    def get(self, args):
        logger.info("Get call to route /etcd with args: {}".format(args))
        try:
            client = EtcdClient(host=conf.host, port=conf.port)

            value = client.get(args["path"]).value

            logger.info(
                "Call to route /etcd successfull returning value: %s", value)
            return {"key": args["path"], "value": value}, 200
        except Exception as e:
            logging.error("Call to route /etcd failed with error: %s", str(e))
            return ({"message": "Error"}, 500)

    @blp_etcd_demo.response(200, EtcdDemoSchema)
    @blp_etcd_demo.response(500)
    @blp_etcd_demo.arguments(EtcdDemoSchema, location="json")
    def post(self, args):
        logger.info("Post call to route /etcd with args: {}".format(args))
        try:
            client = EtcdClient(host=conf.host, port=conf.port)

            client.set(args["path"], args["value"])

            logger.info(
                "Call to route /etcd successfull returning value: %s", args["value"])
            return {"key": args["path"], "value": args["value"]}, 200
        except Exception as e:
            logger.error("Call to route /etcd failed with error: %s", str(e))
            abort(500, message=str(e))

    @blp_etcd_demo.response(200, EtcdQuerySchema)
    @blp_etcd_demo.arguments(EtcdQuerySchema, location="json")
    def delete(self, args):
        logger.info("Delete call to route /etcd with args: {}".format(args))
        try:
            client = EtcdClient(host=conf.host, port=conf.port)

            client.delete(args["path"])

            logger.info(
                "Call to route /etcd successfull returning value: %s", args["path"])
            return {"path": args["path"]}, 200
        except Exception as e:
            logger.error("Call to route /etcd failed with error: %s", str(e))
            abort(500, message=str(e))


@blp_etcd_demo.route("/config")
class EtcdConfigg(MethodView):
    @blp_etcd_demo.response(200, ConfigDemoSchema)
    @blp_etcd_demo.arguments(ConfigQuerySchema, location="query")
    def get(self, args):
        logger.info("Get call to route /config with args: {}".format(args))
        try:
            value = config.get(args["key"])
            logger.info(
                "Call to route /config successfull returning value: %s", value)
            return {"key": args["key"], "value": value}, 200
        except Exception as e:
            logger.error("Call to route /config failed with error: %s", str(e))
            return ({"message": "Error"}, 500)


@blp_metrics.route("/")
class Metrics(MethodView):
    @blp.response(200)
    def get(self):
        logger.info("Get call to route /metrics")
        return ({"application": {
            "db.writes": UserDb.writes, "db.reads": UserDb.reads, "db.cursors": UserDb.cursors}, "base": {}}, 200, {"Content-Type": "application/json"})


@blp_health.route("/disable_db")
class DisableDb(MethodView):
    @blp.response(200)
    def get(self):
        logger.info("Get call to route /disable_db")
        UserDb.has_error = True
        return ("", 200)


@blp_health.route("/live")
class HealthLive(MethodView):
    @blp.response(200, HealthSchema)
    @blp.response(503, HealthSchema)
    @blp.response(500)
    def get(self):
        logger.info("Get call to route /live")
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
            logger.error("Call to route /live failed with error: %s", str(e))
            abort(500)


@blp_health.route("/ready")
class HealthReady(MethodView):
    @blp.response(200, HealthSchema)
    @blp.response(503, HealthSchema)
    @blp.response(500)
    def get(self):
        logger.info("Get call to route /ready")
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
            logger.error("Call to route /ready failed with error: %s", str(e))
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
        logger.info("Post call to route /login")
        try:
            user = UserDb.login(UserLoginSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            logger.error(
                "Call to route /login failed with error: Could not connect to database")
            abort(503, message="Could not connect to database")
        except IncorrectUsernameOrPassword:
            logger.warning(
                "Call to route /login failed with error: Incorrect username or password")
            abort(401, message="Incorrect username or password")
        except Exception as e:
            logger.error("Call to route /login failed with error: %s", str(e))
            abort(404, message=str(e))

        return (user, 200)


@blp.route("/users")
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    @blp.response(404)
    def get(self):
        """Get all users"""
        logger.info("Get call to route /users")
        try:
            users = UserDb.get_all()
        except CouldNotConnectToDatabase:
            logger.error(
                "Call to route /users failed with error: Could not connect to database")
            abort(404, message="Could not connect to database")
        except Exception as e:
            logger.error("Call to route /users failed with error: %s", str(e))
            abort(404, message=str(e))

        return (users, 200)


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    @blp.response(404)
    def get(self, user_id):
        """Get"""
        logger.info("Get call to route /user/%s", user_id)
        try:
            user = UserDb.get_by_id(user_id)
        except CouldNotConnectToDatabase:
            logger.error("Call to route /user/%s failed with error: Could not connect to database", user_id)
            abort(404, message="Could not connect to database")
        except UserNotFound:
            logger.warning("Call to route /user/%s failed with error: User not found", user_id)
            abort(404, message="User not found")
        except Exception as e:
            logger.error("Call to route /user/%s failed with error: %s", user_id, str(e))
            abort(404, message=str(e))

        return (user, 200)

    @blp.arguments(UserRegisterSchema, location="json", as_kwargs=True)
    @blp.response(200, UserSchema)
    @blp.response(404)
    def post(self, _, **args):
        """Register"""
        logger.info("Post call to route /user")
        try:
            user = UserDb.add(UserRegisterSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            logger.error("Call to route /user failed with error: Could not connect to database")
            abort(404, message="Could not connect to database")
        except UserAlreadyExists:
            logger.warning("Call to route /user failed with error: User already exists")
            abort(404, message="User already exists")
        except Exception as e:
            logger.error("Call to route /user failed with error: %s", str(e))
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
api.register_blueprint(blp_etcd_demo)

if __name__ == '__main__':
    logger.debug("Starting LoginRegisterService")
    app.run(port=5002, host="0.0.0.0")
