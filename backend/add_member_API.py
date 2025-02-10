from flask import Flask,request,jsonify
import psycopg2

app = Flask(__name__)

db_config = {
    "dbname":"projectH",
    "user":"postgres",
    "password":"postgres",
    "host":"localhost",
    "port":"5432",
}

def connect_db():
    return psycopg2.connect(**db_config)

@app.route('/addmember',methods=['POST'])
def add_member():
    try:
        data = request.json
        accid = data.get('accid')
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        if not accid or not name or not gender or not age or not age or not height or not weight:
            return jsonify({"success":False,"message":"All data is required"}),400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("insert into members_tbl(account_id,name,gender,age,height,weight) values(%s,%s,%s,%s,%s,%s)",(accid,name,gender,age,height,weight))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success":True,"message":"Member added successfully"}),201
    except psycopg2.errors.ForeignKeyViolation as e:
        return jsonify({"success":False,"message":str(e)}),400
    except psycopg2.errors.InvalidTextRepresentation as e:
        return jsonify({"success":False,"message":str(e)}),400
    except Exception as e:
        return jsonify({"success":False,"message":str(e)}),404

if __name__ == '__main__':
    app.run(debug=True)