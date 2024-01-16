import flask
from flask import send_from_directory

app = flask.Flask(__name__, static_url_path='')

@app.route('/')
def send_openapi():
    return send_from_directory('./', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)