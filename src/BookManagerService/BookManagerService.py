from flask import Flask
from config_managment import CustomConfigManager
from BookManagerDb import BookManagerDb

config = CustomConfigManager("./")
db = BookManagerDb(config)
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello from BookManagerService!"

if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0")
