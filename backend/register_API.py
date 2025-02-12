from flask import Flask,request,jsonify     # Flask for API, request for fetching json data, jsonify for sending data in json
from flask_cors import CORS                 # enables CORS(Cross-origin resource sharing) for all routes
import psycopg2                             # postgreSQL dataAdapter for python
import bcrypt                               # convert password into hash

app = Flask(__name__)           # Initialize Flask app  
CORS(app)                       # Enable CORS to allow requests from different origins

db_config = {                   # database connection variables
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def connect_db():           # databse connection function
    return psycopg2.connect(**db_config)

@app.route('/register',methods=['POST'])            # this is the route from this below function will automatically called
def register_user():
    try:    
        data = request.json         # fetching data from request
        fname = data.get('fname')
        email = data.get('email')
        password = data.get('password')

        if not email or not fname or not password:
            return jsonify({"success":False,"message":"Email,family name and password is required"}),400        # sending message in json formate
        
        hashed_psw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        conn = connect_db()     # connection variable
        cursor = conn.cursor()  # cursor to execute command
        cursor.execute("insert into account_tbl(familyname,email,password_hash) values(%s,%s,%s)",(fname,email,hashed_psw.decode('utf-8')))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success":True,"message":"registration successfully"}),200
    
    except psycopg2.IntegrityError:
        return jsonify({"success":False,"message":"Email already exist"}),400
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),500

if __name__ == '__main__':      # if the file is called accidentally it will not execute
    app.run(debug=True)
