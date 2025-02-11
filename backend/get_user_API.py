from flask import Flask,request,jsonify
import psycopg2

app = Flask(__name__)

db_config = {
    "dbname":"projectH",
    "user":"postgres",
    "password":"postgres",
    "host":"localhost",
    "port":"5432"
}

def connect_db():
    return psycopg2.connect(**db_config)

@app.route('/getuser',methods=['POST'])
def get_user():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        if not email or not name:
            return jsonify({"success":False,"message":"Email and name are required"}),400
        
        conn = connect_db()
        cursor = conn.cursor()
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

if __name__ == '__main__':
    app.run(debug=True)