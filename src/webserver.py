from flask import Flask, request

from flask_cors import CORS

from src.function_query import *
from src.manager_user import *
from src.jwt import *



def create_app(database):
    
    app = Flask(__name__)
    CORS(app)
    
    # initialising the database
    init_db(database)
    def secret_key():
        app.secret_key = "secret"
        return app.secret_key
    key = secret_key()

    
    # example route to check that the connection is correct
    @app.route("/")
    def home():
        return 'Hello World!'
    
    # route that returns all products    
    @app.route("/product")
    def product():
       return get_products()
   
    #route that changes the data of a product
    
    @app.route("/product/upadate/<int:idproduct>", methods=["PATCH"])
    def update_product(idproduct):
        data = request.get_json()
        return change_product(idproduct, data)
    
    # route that returns all products in a category
    @app.route("/category/<category>")
    def categories(category):
        return get_category(category)
    
    #route that returns the data which is include in the form register
    @app.route("/register", methods=["POST"])
    def register():
        key = secret_key()
        data = request.get_json()
        return add_register(data, key)
    
    
    #route that returns all users
    @app.route("/users")
    def get_user():
        return get_users_data()
    
    #route that returns an user
    @app.route("/users/<int:iduser>", methods=['GET'])
    def get_an_user(iduser):
        return get_anuser(iduser)
    
    
    
    #route that returns one user and give the posibility to change the data
    @app.route("/users/change/<int:iduser>", methods=["PATCH"])
    def change_user(iduser):
        data = request.get_json()
        return change_data_user(iduser, data)
    
    #route that delete one user
    @app.route("/users/delete/<int:iduser>", methods=["DELETE"])
    def delete_user(iduser):
        return delete_data_user(iduser)
    
  
    
        

  # TO EXECUTE THE APPLICATION
    if __name__ == '__main__':
        app.run(debug=True)
    # with app.run we're going to indicate that the app is going to be in development
    return app