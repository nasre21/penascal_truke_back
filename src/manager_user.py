import src.database as db
from flask import request, jsonify
import jwt


database_path = ""

# function to connect to the database

def init_db(database):
    global database_path
    database_path = database
    

#Create a new client register
def add_register(data, key):
    con = db.connectdb()
    cursor = con.cursor()
  
    lastname = data['lastname']
    firstname = data['firstname']
    phone = data['phone']
    penascales = data['penascales']
    email = data['email']
    password = data['password']
    payloads = {
        "contraseña": password
    }
    password_encoded = jwt.encode(payloads, key, algorithm="HS256")
    
    data = request.get_json()
      
   
    cursor.execute('INSERT INTO user (lastname, firstname, phone, penascales, email, password) VALUES (%s, %s, %s, %s, %s, %s)',(lastname, firstname, phone, penascales, email, password_encoded))
    
    con.commit()
    con.close()
    print('user added successfully')
    
    return "User created successfully"

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


# function to get an user to obtain the data 
def get_anuser(id_user):
    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM user WHERE iduser = %s', (id_user,))
    data_user = cursor.fetchone()
    
    if data_user:
        data = {'iduser': data_user[0], 'lastname': data_user[1], 'firstname': data_user[2], 'phone': data_user[3], 'sector': data_user[4],'penascales': data_user[5], 'email': data_user[6], 'password': data_user[7]}
        con.close()
        print(data)
        return jsonify(data)
    else:
        return 'The user was not found' 
    

#function to change the data of the users that are in the database for the administrator and database of own user

def change_data_user(id_user, data):
    con = db.connectdb()
    cursor = con.cursor()
    
    if "lastname" in data:
        lastname = data["lastname"]
        cursor.execute('UPDATE user SET lastname = %s WHERE iduser = %s', (lastname, id_user))

    if "firstname" in data:
        firstname = data["firstname"]
        cursor.execute('UPDATE user SET firstname = %s WHERE iduser = %s', (firstname, id_user))

    if "penascales" in data:
        penascales = data["penascales"]
        cursor.execute('UPDATE user SET penascales = %s WHERE iduser = %s', (penascales, id_user))

    if "phone" in data:
        phone = data["phone"]
        cursor.execute('UPDATE user SET phone = %s WHERE iduser = %s', (phone, id_user))

    if "sector" in data:
        sector = data["sector"]
        cursor.execute('UPDATE user SET sector = %s WHERE iduser = %s', (sector, id_user)) 

    if "email" in data:
        email = data["email"]
        cursor.execute('UPDATE user SET email = %s WHERE iduser = %s', (email, id_user))
    
    if "password" in data:
        password = data["password"]
        cursor.execute('UPDATE user SET password = %s WHERE iduser = %s', (password, id_user))   
              
    con.commit()
    con.close()

    return 'Dates modified'

#function to delete one user that are in the database for the administrator
def delete_data_user(id_user):
    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute('DELETE FROM user WHERE iduser = %s', (id_user,))
    con.commit()
    con.close()

    return "User was deleted"
