from flask import Flask,request,jsonify         # Flask for API, request for fetching json data, jsonify for sending data in json
import psycopg2                                 # postgreSQL dataAdapter for python
import bcrypt                                   # convert password into hash

app = Flask(__name__)

db_config = {               # database connection variables
    "dbname":"projectH",
    "user":"postgres",
    "password":"postgres",
    "host":"localhost",
    "port":"5432"
}

def connect_db():           # databse connection function
    return psycopg2.connect(**db_config)

@app.route('/userlogin',methods=['POST'])       # this is the route from this below function will automatically called
def user_login():
    try:
        data = request.json     # fetching data from request
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"success":False,"message":"email and password is required"}),400        # sending message in json formate

        conn = connect_db()         # connection variable
        cursor = conn.cursor()      # cursor to execute command
        cursor.execute("select password_hash from account_tbl where email=%s",(email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            stored_password = row[0]
            if bcrypt.checkpw(password.encode('utf-8'),stored_password.encode('utf-8')):
                return jsonify({"success":True,"message":"Login successfully"}),201
            else:
                return jsonify({"success":False,"message":"Incorrect password"}),400
        else:
            return jsonify({"success":False,"message":"User not found"}),400
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),404

if __name__ == "__main__":      # if the file is called accidentally it will not execute
    app.run(debug=True)