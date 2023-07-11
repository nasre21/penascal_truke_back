import src.database as db
from flask import request

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



def add_register():
    con = db.connectdb()
    cursor = con.cursor()
    data = request.get_json()
    
    lastname = data['lastname']
    firstname = data['firstname']
    phone = data['phone']
    penascales = data['penascales']
    email = data['email']
    password = data['password']
    
    cursor.execute('INSERT INTO peliculas (lastname, firstname, phone, penascales, email, password) VALUES (%s, %s, %s, %s, %s, %s)',(lastname, firstname, phone, penascales, email, password))
    
    con.commit()
    con.close()
    print('user added successfully')
    
