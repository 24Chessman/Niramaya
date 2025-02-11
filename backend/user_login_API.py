from flask import Flask,request,jsonify
import psycopg2
import bcrypt

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

@app.route('/userlogin',methods=['POST'])
def user_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"success":False,"message":"email and password is required"}),400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("select password_hash from account_tbl where email=%s",(email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            stored_password = row[0]
            if bcrypt.hashpw(password.encode('utf-8'),stored_password.encode('utf-8')):
                return jsonify({"success":True,"message":"Login successfully"}),201
            else:
                return jsonify({"success":False,"message":"Incorrect password"}),400
        else:
            return jsonify({"success":False,"message":"User not found"}),400
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),404

if __name__ == "__main__":
    app.run(debug=True)