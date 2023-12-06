from flask import Flask
import dotenv
import os

app = Flask(__name__)

@app.route('/healthcheck')
def healthcheck():
    return "OK", 200

@app.route('/')
def hello():
    return "Hello from BookInfoRetrievalService!"


if __name__ == '__main__':
    config = dotenv.dotenv_values(".env")

    app.run(port=5000, host="0.0.0.0")
