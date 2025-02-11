from flask import Flask,request,jsonify         # Flask for API, request for fetching json data, jsonify for sending data in json
import psycopg2                                 # postgreSQL dataAdapter for python

app = Flask(__name__)

db_config = {                   # database connection variables
    "dbname":"projectH",
    "user":"postgres",
    "password":"postgres",
    "host":"localhost",
    "port":"5432"
}

def connect_db():               # databse connection function
    return psycopg2.connect(**db_config)

@app.route('/getuser',methods=['POST'])         # this is the route from this below function will automatically called
def get_user(): 
    try:
        data = request.json         # fetching data from request
        email = data.get('email')
        name = data.get('name')
        if not email or not name:
            return jsonify({"success":False,"message":"Email and name are required"}),400       # sending message in json formate
        
        conn = connect_db()         # connection variable
        cursor = conn.cursor()      # cursor to execute command
        cursor.execute("select * from members_tbl where name=%s and account_id=(select account_id from account_tbl where email=%s)",(name,email))
        row = cursor.fetchone()

        if row:
            gender = row[3]
            age = row[4]
            height = row[5]
            weight = row[6]
            return jsonify({"success":True,"name":str(name),"gender":str(gender),"age":str(age),"height":str(height),"weight":str(weight)}),201
        else:
            return jsonify({"success":False,"message":"User does not exist"}),400
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),404

if __name__ == '__main__':          # if the file is called accidentally it will not execute
    app.run(debug=True)