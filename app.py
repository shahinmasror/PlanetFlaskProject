from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float,ForeignKey
import  os
from  flask_marshmallow import Marshmallow
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plantetary.db'
db=SQLAlchemy(app)
ma= Marshmallow(app)
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("db created")
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("db dropped")
@app.cli.command('db_seed')
def db_seed():
    mercury=Planet(planet_name='Mercury',
                   planet_type="class b",
                   home_star="sol",
                   mass=4.4,
                   radius=6371,
                   distance=6371,
                   )
    neptune = Planet(planet_name='neptune',
                     planet_type="class c",
                     home_star="sob",
                     mass=4.4,
                     radius=6371,
                     distance=6371,
                     )
    earth = Planet(planet_name='earth',
                     planet_type="class a",
                     home_star="sol",
                     mass=4.4,
                     radius=6371,
                     distance=6371,
                     )



    db.session.add_all([mercury,neptune,earth])


    test_users=User(first_name='Shahin',
                    last_name='Mia',
                    email='s@gmail.com',
                    password='12345')
    db.session.add(test_users)
    db.session.commit()
    print("db seed")


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

@app.route('/planets',methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result=planets_schema.dump(planets_list)
    return jsonify(result)
@app.route('/register',methods=['POST'])
def register():
    email=request.json['email']
    test=User.query.filter_by(email=email).first()
    if test:
        return jsonify(Message='Email already registered'),401
    else:
        first_name=request.json['first_name']
        last_name=request.json['last_name']
        password=request.json['password']
        user=User(first_name=first_name,last_name=last_name,email=email,password=password)

        db.session.add(user)
        db.session.commit()
        return jsonify(Message='User registered'),200





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

class UserSchema(ma.Schema):
   class Meta:
       fields = ('id','first_name','last_name','email','password')
class PlanetSchema(ma.Schema):
    class Meta:
        fields=('planet_id','planet_name','planet_type','home_star','mass','radius','distance')
user_schema = UserSchema()
users_schema = UserSchema(many=True)
planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)









if __name__ == '__main__':
    app.run()
