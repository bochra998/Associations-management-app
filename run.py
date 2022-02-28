from flask import Flask
from flask_cors import CORS, cross_origin
from flask_session import Session

app = Flask(__name__)

sess = Session(app)
CORS(app)

if __name__ == '__main__':
    app.run()
