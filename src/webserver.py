from flask import Flask

from flask_cors import CORS

from src.function_query import *

def create_app(database):
    
    app = Flask(__name__)
    CORS(app)
    
    init_db(database)
    
    @app.route("/")
    def home():
        return 'Hello World!'
    
    