from flask import Flask,request,jsonify     # Flask for API, request for fetching json data, jsonify for sending data in json
import psycopg2                             # postgreSQL dataAdapter for python

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

@app.route('/removeuser',methods=['POST'])      # this is the route from this below function will automatically called
def remove_user():
    try:
        data = request.json         # fetching data from request
        email = data.get('email')
        name = data.get('name')
        if not email or not name:
            return jsonify({"success":False,"message":"Email and name is required"}),400        # sending message in json formate 
        
        conn = connect_db()     # connection variable
        cursor = conn.cursor()  # cursor to execute command
        cursor.execute("delete from members_tbl where name=%s and account_id=(select account_id from account_tbl where email=%s)",(name,email))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"success":True,"message":"Member deleted successfully"}),201
        else:
            return jsonify({"success":False,"message":"Member not found"})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),404

if __name__ == '__main__':      # if the file is called accidentally it will not execute
    app.run(debug=True)