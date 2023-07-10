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
    

  # TO EXECUTE THE APPLICATION
    if __name__ == '__main__':
        app.run(debug=True)
    # with app.run we're going to indicate that the app is going to be in development
    return app