from flask import Flask
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort
from flask_cors import CORS
import requests

from model import BookCompletionQuery, BookCompletionResponse, BookInfoQuery, BookInfoResponse

app = Flask(__name__)
app.config['API_TITLE'] = 'Book info retrieval service'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_JSON_PATH'] = 'openapi.json'

CORS(app)

api = Api(app)
blp = Blueprint("BookInfoRetrievalService", __name__, url_prefix="", description="BookInfoRetrievalService")


api_url_base = "https://hapi-books.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": "318b784573mshd306ec596350becp1958cdjsn699f500710f6",
	"X-RapidAPI-Host": "hapi-books.p.rapidapi.com"
}


@blp.route("/get_name_completion_list")
class BookCompletion(MethodView):
    @blp.arguments(BookCompletionQuery, location="query")
    @blp.response(200, BookCompletionResponse)
    @blp.response(503, description="Could not connect to the api")
    @blp.response(500)
    def get(self, args):
        """ Return list of possible book titles for given partial title """
        try:
            url = api_url_base + f'search/{args["partial"]}'
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                res = response.json()
                completions = []
                for book in res:
                    completions.append(book["name"])
                return {"completions": completions}, 200
            else:
                abort(503, message="Could not connect to the api")
        except Exception as e:
            abort(500, message=str(e))

@blp.route("/get_book_info")
class BookInfo(MethodView):
    @blp.arguments(BookInfoQuery, location="query")
    @blp.response(200, BookInfoResponse)
    @blp.response(503, description="Could not connect to the api")
    @blp.response(500)
    def get(self, args):
        """ Return book info for given title """
        try:
            url = api_url_base + f'search/{args["title"]}'
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                res = response.json()
                if len(res) == 0:
                    abort(404, message="Book not found")
                res = res[0]
                return {
                    "book_id": res["book_id"],
                    "name": res["name"],
                    "cover": res["cover"],
                    "url": res["url"],
                    "authors": res["authors"],
                    "rating": res["rating"],
                    "created_editions": res["created_editions"],
                    "year": res["year"]
                }, 200
            else:
                abort(503, message="Could not connect to the api")
        except Exception as e:
            abort(500, message=str(e))


api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
