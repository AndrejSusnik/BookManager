from flask import Flask
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort
from flask_cors import CORS
from config_managment import CustomConfigManager
import logging
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.handler import LogstashFormatter

from model import BookReviewSchema, BookReviewQuerySchema, BookReviewQueryByUserSchema, BookReviewDb, CouldNotConnectToDatabase, BookReviewNotFound

app = Flask(__name__)
app.config['API_TITLE'] = 'BookManagerService'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_JSON_PATH'] = 'openapi.json'

CORS(app)
api = Api(app)

blp = Blueprint("BookManagerService", __name__, url_prefix="", description="BookManagerService")

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

@blp.route("/book_reviews")
class BookReviews(MethodView):
    @blp.arguments(BookReviewQueryByUserSchema, location="query", as_kwargs=True)
    @blp.response(200, BookReviewSchema(many=True))
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def get(self, **args):
        """Get all book reviews"""
        logger.info("Get call to /book_reviews")
        try:
            book_reviews = BookReviewDb.get_book_reviews(BookReviewQueryByUserSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            logger.error("Could not connect to database")
            abort(503, message="Could not connect to database")
        except Exception as e:
            logger.error("Exception: " + str(e))
            abort(404, message=str(e))

        return (book_reviews, 200)

@blp.route("/book_review")
class BookReview(MethodView):
    @blp.arguments(BookReviewQuerySchema, location="query", as_kwargs=True)
    @blp.response(200, BookReviewSchema)
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def get(self, **args):
        """Get book review"""
        logger.info("Get call to /book_review")
        try:
            book_review = BookReviewDb.get_book_review(BookReviewQuerySchema.from_dict(args))
        except CouldNotConnectToDatabase:
            logger.error("Could not connect to database")
            abort(503, message="Could not connect to database")
        except BookReviewNotFound:
            logger.error("Book review not found")
            abort(404, message="Book review not found")
        except Exception as e:
            logger.error("Exception: " + str(e))
            abort(404, message=str(e))

        return (book_review, 200)

    @blp.arguments(BookReviewSchema, location="json", as_kwargs=True)
    @blp.response(200, BookReviewSchema)
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def post(self, **args):
        """Create book review"""
        logger.info("Post call to /book_review")
        try:
            book_review = BookReviewDb.create_book_review(BookReviewSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            logger.error("Could not connect to database")
            abort(503, message="Could not connect to database")
        except Exception as e:
            logger.error("Exception: " + str(e))
            abort(404, message=str(e))

        return (book_review, 200)

    @blp.arguments(BookReviewSchema, location="json", as_kwargs=True)
    @blp.response(200, BookReviewSchema)
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def put(self, **args):
        """Update book review"""
        logger.info("Put call to /book_review")
        try:
            book_review = BookReviewDb.update_book_review(BookReviewSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            logger.error("Could not connect to database")
            abort(503, message="Could not connect to database")
        except BookReviewNotFound:
            logger.error("Book review not found")
            abort(404, message="Book review not found")
        except Exception as e:
            logger.error("Exception: %s", str(e))
            abort(404, message=str(e))

        return (book_review, 200)

    @blp.arguments(BookReviewQuerySchema, location="json", as_kwargs=True)
    @blp.response(200, BookReviewSchema)
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def delete(self, **args):
        """Delete book review"""
        logger.info("Delete call to /book_review")
        try:
            book_review = BookReviewDb.delete_book_review(BookReviewQuerySchema.from_dict(args))
        except CouldNotConnectToDatabase:
            logger.error("Could not connect to database")
            abort(503, message="Could not connect to database")
        except BookReviewNotFound:
            logger.error("Book review not found")
            abort(404, message="Book review not found")
        except Exception as e:
            logger.error("Exception: " + str(e))
            abort(404, message=str(e))

        return (book_review, 200)


api.register_blueprint(blp)

if __name__ == '__main__':
    logger.info("Starting BookManagerService")
    app.run(port=5001, host="0.0.0.0")
