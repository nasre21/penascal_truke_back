import src.database as db
from flask import request
import jwt


database_path = ""

# function to connect to the database

def init_db(database):
    global database_path
    database_path = database
    

# function to get all the products from the database, returns them in an array

def get_products():
    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM user")
    myusers = cursor.fetchall()
    product_array = []
    product_col_Names = [column[0] for column in cursor.description]
    for product in myusers:
        product_array.append(dict(zip(product_col_Names, product)))

    cursor.close()
    return product_array

# function to get all the products of a specific category from the database, returns them in array

def get_category(category):
    con = db.connectdb()
    cursor = con.cursor()
    select_query = "SELECT * FROM product WHERE category = %s"
    cursor.execute(select_query, (category,))
    myproducts = cursor.fetchall()
    product_array = []
    product_col_Names = [column[0] for column in cursor.description]
    for product in myproducts:
        product_array.append(dict(zip(product_col_Names, product)))
    cursor.close()
    return product_array

# function to get all the users that are in the database for the administrator
def get_users_data():
    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM user")
    myusers = cursor.fetchall()
    product_array = []
    product_col_Names = [column[0] for column in cursor.description]
    for product in myusers:
        product_array.append(dict(zip(product_col_Names, product)))

    cursor.close()
    return product_array



# def add_register(request, key):
#     lastname = request.form['lastname']
#     firstname = request.form['firstname']
#     phone = request.form['phone']
#     penascales = request.form['penascales']
#     email = request.form['email']
#     password = request.form['password']
    
#     payloads = {
#         "contraseña": password
#     }
    
#     # data = request.get_json()
    
#     con = db.connectdb()
#     cursor = con.cursor()
    
#     password_encoded = jwt.encode(payloads, key, algorithm="HS256")
   
#     cursor.execute('INSERT INTO user (lastname, firstname, phone, penascales, email, password) VALUES (%s, %s, %s, %s, %s, %s)',(lastname, firstname, phone, penascales, email, password_encoded))
    
#     con.commit()
#     con.close()
#     print('user added successfully')
    
#     return "User created successfully"

def add_register(data):
    con = db.connectdb()
    cursor = con.cursor()
  
    lastname = data['lastname']
    firstname = data['firstname']
    phone = data['phone']
    penascales = data['penascales']
    email = data['email']
    password = data['password']
    
    data = request.get_json()
      
   
    cursor.execute('INSERT INTO user (lastname, firstname, phone, penascales, email, password) VALUES (%s, %s, %s, %s, %s, %s)',(lastname, firstname, phone, penascales, email, password))
    
    con.commit()
    con.close()
    print('user added successfully')
    
    return "User created successfully"