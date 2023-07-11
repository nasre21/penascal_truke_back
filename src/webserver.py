from flask import Flask, request

from flask_cors import CORS

from src.function_query import *

def create_app(database):
    
    app = Flask(__name__)
    CORS(app)
    
    # initialising the database
    init_db(database)
    
    
    # example route to check that the connection is correct
    @app.route("/")
    def home():
        return 'Hello World!'
    
    # route that returns all products    
    @app.route("/product", methods=['GET', 'POST'])
    def product():
        if request.method == 'POST':
            return ""
        else:
            return get_products()
    
    # route that returns all products in a category
    @app.route("/category/<category>")
    def categories(category):
        return get_category(category)
    
    @app.route("/users")
    def get_user():
        return get_users_data()
    
    @app.route("/register", methods=["POST"])
    def register():
        return register_add()
    
    
    
    
    

  # TO EXECUTE THE APPLICATION
    if __name__ == '__main__':
        app.run(debug=True)
    # with app.run we're going to indicate that the app is going to be in development
    return app