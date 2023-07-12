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



# function to change a product
def change_product(id_product, data):
    con = db.connectdb()
    cursor = con.cursor()
    
    if "photo" in data:
        photo = data["photo"]
        cursor.execute('UPDATE product SET photo = %s WHERE idproduct = %s', (photo, id_product))

    if "name" in data:
        name = data["name"]
        cursor.execute('UPDATE product SET name = %s WHERE idproduct = %s', (name, id_product))

    if "description" in data:
        description = data["description"]
        cursor.execute('UPDATE product SET description = %s WHERE idproduct = %s', (description, id_product))

    if "price" in data:
        price = data["price"]
        cursor.execute('UPDATE product SET price = %s WHERE idproduct = %s', (price, id_product))

    if "category" in data:
        category = data["category"]
        cursor.execute('UPDATE product SET category = %s WHERE idproduct = %s', (category, id_product)) 

              
    con.commit()
    con.close()

    return 'Dates modified'


# function to delete a product

def delete_data_product(idproduct):
    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute('DELETE FROM product WHERE idproduct = %s', (idproduct,))
    con.commit()
    con.close()
    return 'Product deleted'


