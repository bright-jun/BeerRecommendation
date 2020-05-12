import json
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Resource, Api, request
from pyrebase import pyrebase

config = {
    'apiKey': "AIzaSyCgXMUR5gG6ycHlaxx5gbgdHvl2blsdN5A",
    'authDomain': "macfilx.firebaseapp.com",
    'databaseURL': "https://macfilx.firebaseio.com",
    'projectId': "macfilx",
    'storageBucket': "macfilx.appspot.com",
    'messagingSenderId': "379222478610",
    'appId': "1:379222478610:web:c78eb8631919d6b3"
};
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('bid', type=int)
parser.add_argument('cid', type=int)
parser.add_argument('name', type=str)
parser.add_argument('email', type=str)
parser.add_argument('pass', type=str)


class ColumnFromCid(Resource):
    def post(self):
        args = parser.parse_args()
        with open('column.json') as json_file:
            cid = int(args['cid'] - 1)
            json_data = json.load(json_file)
            return jsonify(json_data[cid]['title'])
    def get(self):
        return {'result': 'getok'}

class BeerdataFromBid(Resource):
    
    def post(self):
        args = parser.parse_args()
        with open('data.json') as json_file:
            bid = int(args['bid'] - 1)
            json_data = json.load(json_file)
            return jsonify(json_data[bid]['name'])
            '''
    def post(self):
        beername = "Asahi"
        group = db.child("0").child(beername).child("group").get().val()
        IBU = db.child("0").child(beername).child("IBU").get().val()
        ABV = db.child("0").child(beername).child("ABV").get().val()
        SRM = db.child("0").child(beername).child("SRM").get().val()
        labels_64 = db.child("0").child(beername).child("labels_64").get().val()
        rating = db.child("0").child(beername).child("rating").get().val()
        return {'1':group,'2':IBU,'3':ABV,'4':SRM,'5':labels_64,'6':rating}
    '''
    def get(self):
        return {'result': 'getbeer'}

class Register(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        email = args['email']
        passw = args['pass']
        try:
            auth.create_user_with_email_and_password(email,passw)
        except:
            message="Unable to create account try again"
            return {'result':'fail'}
        return {'result':'true'}
    def get(self):
        return {'result': 'getbeer'}

api.add_resource(Register, '/register')
api.add_resource(ColumnFromCid, '/column')
api.add_resource(BeerdataFromBid, '/beer')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)
