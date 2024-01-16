i
from flask import Flask, request, jsonify, make_response
from decouple import config

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route("/test")
def test():
    try:
        db.session.query(User).first()
        print("Databases connection successful.")
    except:
        print("DB connection failed.")
    return "Testing"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return (jsonify({'error': 'Username and password are required'}), 400)

    new_user = User(username=username, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return (jsonify({'message': 'User created successfully'}), 201)
    except:
        db.session.rollback()
        return (jsonify({'error': 'Error creating user'}), 500)

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    
    print(username,password)

    user = User.query.filter_by(username=username).first()
    is_match=user.password==password

    if is_match:
        return (jsonify({'message': 'Login successful'}), 200)
    else:
        return (jsonify({'error': 'Invalid username or password'}), 401)


# @app.route("/users", methods= ["GET"])
# def get_users():
#     users = User.query.all()
#     data = [user.json() for user in users]
#     return make_response(jsonify({"data":data}), 200)

@app.before_request
def db_init():
    with app.app_context():
        db.create_all()
        db.session.commit()