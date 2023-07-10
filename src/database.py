#THAT IS THE FILE database.py WHICH CONNECT WITH THE DATABASE

#1. We need is a connector: mysql-conector

import mysql.connector

def connectdb():
    host = "containers-us-west-2.railway.app"
    user = "root"
    password = "Vpc9U35FL63X8CRJowuL"
    database = "railway"
    port = 6140
    
    try:
        con = mysql.connector.connect(
            host=host, 
            user=user, 
            password=password, 
            database= database, 
            port=port)
        print("Connected to database")
        
        return con
        
    except mysql.connector.Error as error:
        print(f"Failed to connect to database: {error}")
        
        return None
    
    # Try that the function connects to the database with correct credentials and returns a connection object
    # Except that the function returns None when connecting to a non-existent database