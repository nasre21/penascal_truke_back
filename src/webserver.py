from flask import Flask, request

from flask_cors import CORS

from src.function_query import *
from src.manager_user import *
from src.jwt import *


def create_app(database):
    
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

    
    # initialising the database
    init_db(database)


    # example route to check that the connection is correct
    @app.route("/")
    def home():
        return 'Hello World!'
    
    # route that returns all products    
    @app.route("/product")
    def product():
       return get_products()
      
    #route that returns a product
    @app.route("/product/<int:idproduct>")
    def get_a_product(idproduct):
        return get_one_product(idproduct)
   
    #route that changes the data of a product
    
    @app.route("/product/upadate/<int:idproduct>", methods=["PATCH"])
    def update_product(idproduct):
        data = request.get_json()
        return change_product(idproduct, data)
    
    # route join product with user
    @app.route("/product/user/<product_id>", methods=["GET"])
    def join_product(product_id):
        return join_product_user(product_id)
    
    #route that delete one user
    @app.route("/product/delete/<int:idproduct>", methods=["DELETE"])
    def delete_product(idproduct):
        return delete_data_product(idproduct)
    
    # route that returns all products in a category
    @app.route("/category/<category>")
    def categories(category):
        return get_category(category)
    
    #route that returns the data which is include in the form card product 
    @app.route("/createproduct",methods=["POST"])
    def createproduct():
         data = request.get_json()
         return create_product(data)
    
   #route that returns the data which is include in the form register
    @app.route("/register", methods=["POST"])
    def register():
        key = secret_key()
        data = request.get_json()
        return add_register(data, key)

        
    # route that returns the data which is include in the form login
    @app.route("/login", methods=["POST"])
    def login():
        key = secret_key()
        data = request.get_json()
        return login_user(data,key)
    
    #router that check the admin email and password 
    @app.route("/admin", methods=["POST"])
    def adm_login():
        key = secret_key()
        data = request.get_json()
        return login_admin(data, key)
    
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
    
    
    # route for join user with seller
    @app.route("/users/seller/<int:idseller>", methods=["GET"])
    def join_user(idseller):
        return join_data_seller(idseller)
    
     
    return app


        