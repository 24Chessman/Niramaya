from flask import Flask,request,jsonify         # Flask for API, request for fetching json data, jsonify for sending data in json
from flask_cors import CORS                     # enables CORS(Cross-origin resource sharing) for all routes
import psycopg2                                 # postgreSQL dataAdapter for python

app = Flask(__name__)           # Initialize Flask app  
CORS(app)                       # Enable CORS to allow requests from different origins

db_config = {                   # database connection variables
    "dbname":"projectH",
    "user":"postgres",
    "password":"postgres",
    "host":"localhost",
    "port":"5432",
}

def connect_db():           # databse connection function
    return psycopg2.connect(**db_config)

@app.route('/addmember',methods=['POST'])           # this is the route from this below function will automatically called
def add_member():
    try:
        data = request.json         # fetching data from request
        accid = data.get('accid')
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        if not accid or not name or not gender or not age or not age or not height or not weight:
            return jsonify({"success":False,"message":"All data is required"}),400          # sending message in json formate

        conn = connect_db()         # connection variable
        cursor = conn.cursor()      # cursor to execute command
        cursor.execute("insert into members_tbl(account_id,name,gender,age,height,weight) values(%s,%s,%s,%s,%s,%s)",(accid,name,gender,age,height,weight))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success":True,"message":"Member added successfully"}),200
    except psycopg2.errors.ForeignKeyViolation as e:
        return jsonify({"success":False,"message":str(e)}),400
    except psycopg2.errors.InvalidTextRepresentation as e:
        return jsonify({"success":False,"message":str(e)}),400
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),500

if __name__ == '__main__':          # if the file is called accidentally it will not execute
    app.run(debug=True)