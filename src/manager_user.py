import src.database as db
from flask import request, jsonify, session
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
        if lastname:
            cursor.execute('UPDATE user SET lastname = %s WHERE iduser = %s', (lastname, id_user))

    if "firstname" in data:
        firstname = data["firstname"]
        if firstname:
            cursor.execute('UPDATE user SET firstname = %s WHERE iduser = %s', (firstname, id_user))

    if "penascales" in data:
        penascales = data["penascales"]
        if penascales:
            cursor.execute('UPDATE user SET penascales = %s WHERE iduser = %s', (penascales, id_user))

    if "phone" in data:
        phone = data["phone"]
        if phone:
            cursor.execute('UPDATE user SET phone = %s WHERE iduser = %s', (phone, id_user))

    if "sector" in data:
        sector = data["sector"]
        if sector:
            cursor.execute('UPDATE user SET sector = %s WHERE iduser = %s', (sector, id_user)) 

    if "email" in data:
        email = data["email"]
        if email:
            cursor.execute('UPDATE user SET email = %s WHERE iduser = %s', (email, id_user))
    
    if "password" in data:
        password = data["password"]
        if password:
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

#function to login the user

def login_user(data, key):
    
    user_email = data['email']
    user_password = data['password']
    print("data que obtenemos", user_password)

    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM user WHERE email = %s', (user_email,))
    result = cursor.fetchone()

    if result is not None:
        user_email_db = result[6]
        user_password_db = result[7]
        print(user_password_db)
        print(user_email_db)
        
        decoded_token = jwt.decode(user_password_db, key, algorithms=["HS256"])

        # Assuming user_password_db contains the JWT token
        if user_email_db == user_email and decoded_token['contraseña'] == user_password:
            #session['user_email_db'] = user_email
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
        return 'User not found'  # Return a response for the case when the user is not found in the database
        
    
    
# register a new admin
def add_register_admin(data, key):
    con = db.connectdb()
    cursor = con.cursor()
  
    name = data['name']
    email = data['email']
    password = data['password']
    
    payloads = {
        "contraseña": password
    }
    password_encoded = jwt.encode(payloads, key, algorithm="HS256")
    
    data = request.get_json()
      
   
    cursor.execute('INSERT INTO admin (name, email, password) VALUES (%s, %s, %s)',(name,email, password_encoded))
    
    con.commit()
    con.close()
    print('user added successfully')
    
    return "User created successfully"


def admin_login_data(data, key):
    adm_email = data['email']
    adm_password = data['password']
    print("data que obtenemos", adm_email)
    print("data que obtenemos", adm_password)

    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM admin WHERE email = %s', (adm_email,))
    result = cursor.fetchone()

    if result is not None:
        adm_email_db = result[2]
        adm_password_db = result[3]
        print("esto es email de la base datos", adm_email_db)
        print("esto es password de la base de datos", adm_password_db)
        

        decoded_token = jwt.decode(adm_password_db, key, algorithms=["HS256"])
        
        print("esto es la contraseña", decoded_token)
        
        print("esto es la contraseña desencriptada", decoded_token['contraseña'])

        # Assuming adm_password_db contains the JWT token
        if adm_email_db == adm_email and decoded_token['contraseña'] == adm_password:
            # session['adm_email_db'] = adm_email_db
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
        return 'Admin not found'  # Return a response for the case when the admin is not found in the data

def join_data_seller(idseller):
    con = db.connectdb()
    cursor = con.cursor()

    query = """
        SELECT *
        FROM user
        INNER JOIN seller ON user.seller_id = seller.idseller
        WHERE user.iduser =%s;
    """
    cursor.execute(query, (idseller,))
    result = cursor.fetchone()

    cursor.close()
    con.close()

    if result:
        user = {
            'iduser': result[0],
            'lastname': result[1],
            'firstname': result[2],
            'phone': result[3],
            'sector': result[4],
            'penascales': result[5],
            'email': result[6],
            'idseller': result[8],
            'userid': result[9],
            'productid': result[10],
        }
        return user
    else:
        return None

# get admin data
def get_admin_data(id_admin):
    con = db.connectdb()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM admin WHERE idadmin = %s", (id_admin,))
    data_admin = cursor.fetchone()
    
    if data_admin:
        data = {'idadmin': data_admin[0], 'name': data_admin[1], 'email': data_admin[2], 'password': data_admin[3]}
        con.close()
        print(data)
        return jsonify(data)
    else:
        return 'The admin was not found' 
