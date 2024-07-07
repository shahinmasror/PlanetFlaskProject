from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float,ForeignKey
import os
from  flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
from flask_mail import Mail,Message
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plantetary.db'
app.config['JWT_SECRET_KEY']='super_secret'
"""
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
"""
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '1d7732b954cb8a'
app.config['MAIL_PASSWORD'] = '595805e5a8b8db'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db=SQLAlchemy(app)
ma= Marshmallow(app)
jwt=JWTManager(app)
mail = Mail(app)
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

@app.route('/login',methods=['POST'])
def login():
    if request.is_json:
        email=request.json['email']
        password=request.json['password']
    else:
        email=request.form['email']
        password=request.form['password']

    test=User.query.filter_by(email=email,password=password).first()
    if test:
           access_token = create_access_token(identity=email)
           return jsonify(Message='Loging Success' ,access_token=access_token)
    else:
        return jsonify(Message='Email or Password is incorrect'),401
""""

@app.route('/send_email')
def send_email():
  msg = Message(
    'Hello',
    recipients=['shahinmasror.tb@gmail.com'],
    body='This is a test email sent from Flask-Mail!'
  )
  mail.send(msg)
  return 'Email sent succesfully!'
  """

@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message(
            "Your planetary password",
            body=f"Your planetary password is: {user.password}",
            sender="admin@planetary-api.com",
            recipients=[email]
        )
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="Email not found"), 404


@app.route('/get_planetbyid/<int:planet_id>', methods=['GET'])
def get_planetbyid(planet_id: int):
    data = Planet.query.filter_by(planet_id=planet_id).first()
    if data:
        planet_schema = PlanetSchema()
        result = planet_schema.dump(data)
        return jsonify(result), 200
    else:
        return jsonify(message="Planet not found"), 404

@app.route('/add_palnet', methods=['POST'])
@jwt_required()
def add_palnet():
    planet_name = request.json['planet_name']
    result = Planet.query.filter_by(planet_name=planet_name).first()
    if result:
        return jsonify(message="Plants already exists"), 401
    else:
        planet_type = request.json['planet_type']
        home_star = request.json['home_star']
        mass = request.json['mass']
        radius = request.json['radius']

        distance = request.json['distance']
        new_planet=Planet(
            planet_name=planet_name,
            planet_type=planet_type,
            home_star=home_star,
            mass=mass,
            radius=radius,
            distance=distance
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message="Plants added successfully")


@app.route('/update_planet', methods=['PUT'])
@jwt_required()
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet=Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        Planet.planet_name = request.form['planet_name']
        Planet.planet_type = request.form['planet_type']
        Planet.home_star = request.form['home_star']
        Planet.mass= float(request.form['mass'])
        Planet.radius= float(request.form['radius'])
        Planet.distance = float(request.form['distance'])

        db.session.commit()


        return jsonify(message="Plants updated successfully"),200
    else:
        return jsonify(message="Plants not found"), 404

@app.route('/delete_planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id:int):

    planet=Planet.query.filter_by(planet_id=planet_id).first()

    if planet:
        db.session.delete(planet)
        db.session.commit()

        return jsonify(message="Plants deleted successfully")










if __name__ == '__main__':
    app.run()
