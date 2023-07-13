import src.database as db
from flask import request, jsonify, session
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
    cursor.execute("SELECT * FROM product")
    myproducts = cursor.fetchall()
    product_array = []
    product_col_Names = [column[0] for column in cursor.description]
    for product in  myproducts:
        product_array.append(dict(zip(product_col_Names, product)))

    cursor.close()
    return product_array

# function to get all the products of a specific category from the database, returns them in array

def get_category(category):
    con = db.connectdb()
    cursor = con.cursor()
    select_query = "SELECT * FROM product WHERE category = %s"
    cursor.execute(select_query, (category,))
    mycategory = cursor.fetchall()
    categorys_array = []
    categorys_col_Names = [column[0] for column in cursor.description]
    for categorys in mycategory:
        categorys_array.append(dict(zip(categorys_col_Names, categorys)))
    cursor.close()
    return categorys_array



# function to get all the users that are in the database for the administrator
def get_users_data():
    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM user")
    myusers = cursor.fetchall()
    user_array = []
    user_col_Names = [column[0] for column in cursor.description]
    for user in myusers:
        user_array.append(dict(zip(user_col_Names, user)))

    cursor.close()
    return user_array

#funtion to get one product
def get_one_product(id_product):
    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM product WHERE idproduct = %s', (id_product,))
    data_product = cursor.fetchone()
    
    if data_product:
        data = {'idproduct': data_product[0], 'photo': data_product[1], 'name': data_product[2], 'description': data_product[3], 'price': data_product[4],'category': data_product[5]}
        con.close()
        print(data)
        return jsonify(data)
    else:
        return 'The product was not found' 
    
#funtion to create a product
def create_product(data):
    con = db.connectdb()
    cursor = con.cursor()
    data = request.get_json()
    photo = data["photo"]
    name = data["name"]
    description = data["description"]
    price = data["price"]
    category = data["category"]
    cursor.execute('INSERT INTO product (photo, name, description, price, category) VALUES (%s, %s, %s, %s, %s)', (photo, name, description, price, category))
    con.commit()
    con.close()
    
    print('product added successfully')
    
    return "Product created successfully"
    
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

# function to check the admin email and password if it is correct
#function to login the user

def login_admin(data, key):
    adm_email = data['email']
    adm_password = data['password']
    print("Data obtained:", adm_password)

    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM admin WHERE email = %s', (adm_email,))
    result = cursor.fetchone()

    if result is not None:
        adm_email_db = result[2]
        jwt_token_db = result[3]  # Assumes the JWT token is stored in the database
        print("Stored JWT token:", jwt_token_db)
        print("Stored email:", adm_email_db)

        try:
            decoded_token = jwt.decode(jwt_token_db, key, algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            con.commit()
            con.close()
            return 'Login failed'  # Return a response indicating login failure

        if decoded_token['email'] == adm_email_db and adm_password == decoded_token['password']:
            session['adm_email_db'] = adm_email_db
            con.commit()
            con.close()
            return 'Login successful'  # Return a response indicating success
        else:
            con.commit()
            con.close()
            return 'Login failed'  # Return a response indicating login failure

    else:
        con.commit()
        con.close()
        return 'Admin not found'

