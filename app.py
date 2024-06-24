from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float,ForeignKey
import  os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plantetary.db'
db=SQLAlchemy(app)

@app.route('/sample_api')

def sample_api():
    return jsonify(Message='Bangladesh Win'),200
@app.route('/not_found')
def not_found():
    return jsonify(Message='Not Found'),404
@app.route('/paramerter')
def param():
    name=request.args.get('name')
    age=int(request.args.get('age'))
    if(age<18):
        return jsonify(Message='You are Mr.'+name+', Not Allowed '),401
    else:
        return jsonify(Message='You are Mr.'+name+'Allowed'),200

@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name:str,age:int):
    if (age < 18):
        return jsonify(Message='You are Mr.' + name + ', Not Allowed '), 401
    else:
        return jsonify(Message='You are Mr.' + name + 'Allowed'), 200


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star=Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)







if __name__ == '__main__':
    app.run()