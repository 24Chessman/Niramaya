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

@app.route('/removeuser',methods=['POST'])
def remove_user():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        if not email or not name:
            return jsonify({"success":False,"message":"Email and name is required"}),400
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("delete from members_tbl where name=%s and account_id=(select account_id from account_tbl where email=%s)",(name,email))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"success":True,"message":"Member deleted successfully"}),201
        else:
            return jsonify({"success":False,"message":"Member not found"})
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),404

if __name__ == '__main__':
    app.run(debug=True)