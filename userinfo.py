from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app= Flask (__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}},supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URI','postgresql://postgres:success@localhost:5432/Flask_db')
app.config['SQLALCHEMY_TRACK_DATABASE']=False

db=SQLAlchemy(app)


class UserInfo(db.Model):
    __tablename__ = "usersinfo"

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    first_name=db.Column(db.String(50), unique=False, nullable=False)
    last_name=db.Column(db.String(50),unique=False,nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    address=db.Column(db.String(50),unique=False,nullable=False)


@app.route('/homepage')
def check():
    return ("Homepage")

# same route get and post 
@app.route('/userinfo', methods=['POST'])
def info():

    data = request.get_json()
    username=data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    address = data.get('address')

    information=UserInfo(username=username,first_name=first_name,last_name=last_name,email=email,address=address)

    try:
        db.session.add(information)
        db.session.commit()
        return (jsonify({"message": "Information added"}), 200)
    except Exception as e:
        print(e)
        db.session.rollback()
        return (jsonify({"message": "Error updating the data"}), 500)
    
@app.route('/getinfo',methods=['GET'])
def getinfo():
    users=UserInfo.query.all()
    data = [
        {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'address': user.address
        }
        for user in users
    ]
    # data= [user.json() for user in users]
    return (jsonify({"data":data}),200)

@app.route('/update/<username>',methods=['PUT','PATCH'])
def updateinfo(username):
    user = UserInfo.query.filter_by(username=username).first()

    if not user:
        return (jsonify({'error': 'User not found'}), 400)
    
    data = request.get_json()

    if 'first_name' in data:
        user.first_name=data['first_name']
    if 'last_name' in data:
        user.last_name=data['last_name']
    if 'email' in data:
        user.email=data['email']
    if 'address' in data:
        user.address=data['address']
    try:
        db.session.commit()
        return (jsonify({"message": "Information updated"}), 200)
    except Exception as e:
        print(e)
        db.session.rollback()
        return (jsonify({"message": "Error updating the data"}), 500)


@app.route("/delete/<username>",methods=['DELETE'])
def delete(username):
    user=UserInfo.query.filter_by(username=username).first()

    if not user:
        return (jsonify({'message':'user not found to delete'}))
    
    try:
        db.session.delete(user)
        db.session.commit()
        return (jsonify({'message':'user assassined'}),200)
    except Exception as e:
        print (e)
        db.session.rollback()
        return (jsonify({'message':'Can\'t delete this'}),500)

@app.before_request 
def db_init():
    with app.app_context():
        db.create_all()
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
