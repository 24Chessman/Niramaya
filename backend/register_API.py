from flask import Flask,request,jsonify
import psycopg2
import bcrypt


app = Flask(__name__)

db_config = {
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def connect_db():
    return psycopg2.connect(**db_config)

@app.route('/register',methods=['POST'])
def register_user():
    try:
        data = request.json
        fname = data.get('fname')
        email = data.get('email')
        password = data.get('password')

        if not email or not fname or not password:
            return jsonify({"success":False,"message":"Email,family name and password is required"}),400
        
        hashed_psw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("insert into account_tbl(familyname,email,password_hash) values(%s,%s,%s)",(fname,email,hashed_psw.decode('utf-8')))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success":True,"message":"registration successfully"}),201
    
    except psycopg2.IntegrityError:
        return jsonify({"success":False,"message":"Email already exist"}),400
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),500

if __name__ == '__main__':
    app.run(debug=True)
