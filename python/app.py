import os
from flask import Flask , render_template
from flask_cors import CORS, cross_origin
import pymysql
import mysql.connector  
from mysql.connector import Error 
import json 
from flask import jsonify
from flask import  request
from werkzeug.security import generate_password_hash, check_password_hash
from elasticsearch import Elasticsearch , helpers

app = Flask(__name__)
app.secret_key = "secret key"

CORS(app)
""" app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'userstlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
 """

def connect():
	try:
		conn = mysql.connector.connect(
			user=os.getenv("MYSQL_USER"), 
			password=os.getenv("MYSQL_PASSWORD"), 
			host=os.getenv("MYSQL_HOST"),
			database=os.getenv("MYSQL_DB")
			)
		return conn
	except Exception as e :
		print('error while connecting to mysql',e)

@app.route('/')
def users1():
	connection = connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	cursor.execute('SELECT * FROM tbl_user ')
	users= cursor.fetchall()
	
	return users

@app.route('/add', methods=['POST'])
def add_user():
	connection = None
	cursor = None
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			connection=connect()
			cursor = connection.cursor()
			cursor.execute(sql, data)
			connection.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		connection.close()
		
@app.route('/users')
def users():
	connection = None
	cursor = None
	try:
		connection=connect()
		cursor = connection.cursor()
		cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd FROM tbl_user")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		connection.close()
	
		
@app.route('/user/<int:id>')
def user(id):
	connection = None
	cursor = None
	try:
		connection=connect()
		cursor = connection.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd FROM tbl_user WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		connection.close()

@app.route('/update', methods=['PUT'])
def update_user():
	connection = None 
	cursor = None
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']		
		# validate the received values
		if _name and _email and _password and _id and request.method == 'PUT':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			connection=connect()
			cursor = connection.cursor()
			cursor.execute(sql, data)
			connection.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		connection.close()
		
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
	connection = None 
	cursor = None
	try:
		connection=connect()
		cursor = connection.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		connection.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		connection.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

ELASTIC_URL= 'http://localhost:9200' 

es = Elasticsearch(ELASTIC_URL)
print(es.ping)
INDEX_NAME="offre"
def create_index(self) -> None:
        body={}
        try:
            result=es.indices.create(index= INDEX_NAME,body=body,ignore=400)
            if 'error' in result:
                return 2
            else:
                return 1
        except:
            return  0


def addDoc(self, doc:dict)->bool:
	try:
		es.index(index=INDEX_NAME,document=doc,pipeline=None)
		return True
	except Exception as e:
		print(e)
		return False
def deleteDoc (id:str)->bool:
	try:
		es.delete(index=INDEX_NAME, id=id)	
		return True
	except Exception as e:
		print (e)
		return False 
def updateDocById( id:str , doc:dict)->bool:
	try:
		resp=es.index(index=INDEX_NAME,id=id)
		return True
	except Exception as e :
		print (e)
		return False

@app.route("/offres",methods=['POST'])
def insert_Offre(request_json:dict) -> dict:
	body=request.json
	res=addDoc(index='offre',doc=body)
	print(body)
	return  jsonify({
            'status': 'Data is posted to elasticsearch !',
        })

if __name__ == "__main__":
    app.run(debug=True)