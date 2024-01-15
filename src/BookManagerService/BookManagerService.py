from flask import Flask
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort
from flask_cors import CORS

from model import BookReviewSchema, BookReviewQuerySchema, BookReviewQueryByUserSchema, BookReviewDb, CouldNotConnectToDatabase, BookReviewNotFound

app = Flask(__name__)
app.config['API_TITLE'] = 'BookManagerService'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

CORS(app)
api = Api(app)

blp = Blueprint("BookManagerService", __name__, url_prefix="/BookManagerService", description="BookManagerService")

@blp.route("/book_reviews")
class BookReviews(MethodView):
    @blp.arguments(BookReviewQueryByUserSchema, location="query", as_kwargs=True)
    @blp.response(200, BookReviewSchema(many=True))
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def get(self, **args):
        """Get all book reviews"""
        try:
            book_reviews = BookReviewDb.get_book_reviews(BookReviewQueryByUserSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            abort(503, message="Could not connect to database")
        except Exception as e:
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
        try:
            book_review = BookReviewDb.get_book_review(BookReviewQuerySchema.from_dict(args))
        except CouldNotConnectToDatabase:
            abort(503, message="Could not connect to database")
        except BookReviewNotFound:
            abort(404, message="Book review not found")
        except Exception as e:
            abort(404, message=str(e))

        return (book_review, 200)

    @blp.arguments(BookReviewSchema, location="json", as_kwargs=True)
    @blp.response(200, BookReviewSchema)
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def post(self, **args):
        """Create book review"""
        try:
            book_review = BookReviewDb.create_book_review(BookReviewSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            abort(503, message="Could not connect to database")
        except Exception as e:
            abort(404, message=str(e))

        return (book_review, 200)

    @blp.arguments(BookReviewSchema, location="json", as_kwargs=True)
    @blp.response(200, BookReviewSchema)
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def put(self, **args):
        """Update book review"""
        try:
            book_review = BookReviewDb.update_book_review(BookReviewSchema.from_dict(args))
        except CouldNotConnectToDatabase:
            abort(503, message="Could not connect to database")
        except BookReviewNotFound:
            abort(404, message="Book review not found")
        except Exception as e:
            abort(404, message=str(e))

        return (book_review, 200)

    @blp.arguments(BookReviewQuerySchema, location="query", as_kwargs=True)
    @blp.response(200, BookReviewSchema)
    @blp.response(404)
    @blp.response(503, description="Could not connect to database")
    def delete(self, **args):
        """Delete book review"""
        try:
            book_review = BookReviewDb.delete_book_review(BookReviewQuerySchema.from_dict(args))
        except CouldNotConnectToDatabase:
            abort(503, message="Could not connect to database")
        except BookReviewNotFound:
            abort(404, message="Book review not found")
        except Exception as e:
            abort(404, message=str(e))

        return (book_review, 200)


api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0")
