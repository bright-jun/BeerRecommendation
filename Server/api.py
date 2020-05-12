import json
import csv
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Resource, Api, request
from Main import get_recommendation_list
from pyrebase import pyrebase
from operator import eq
import random


config = {
    'apiKey': "AIzaSyCgXMUR5gG6ycHlaxx5gbgdHvl2blsdN5A",
    'authDomain': "macfilx.firebaseapp.com",
    'databaseURL': "https://macfilx.firebaseio.com",
    'projectId': "macfilx",
    'storageBucket': "macfilx.appspot.com",
    'messagingSenderId': "379222478610",
    'appId': "1:379222478610:web:c78eb8631919d6b3"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
'''
def find_uid(email):
    with open('userdata.csv', 'r') as user_data:
        rdr = csv.reader(user_data)
        for line in rdr:
            if email == line[1]:
                return int(line[2])
    return 1

    all_users = db.child("user").get()
    for user in all_users.each():
        if eq(db.child("user").child(user.key()).child("name").get().val(), name):
            return db.child("user").child(user.key()).child("uid").get().val()
'''
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('bid', type=int)
parser.add_argument('uid', type=int)
parser.add_argument('cid', type=int)
parser.add_argument('name', type=str)
parser.add_argument('email', type=str)
parser.add_argument('pass', type=str)
parser.add_argument('rating', type=int)



class MyLogin(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        passw = args['pass']
        db_pass = db.child("users").child(name).child("pw").get().val()
        if passw == db_pass:
            name = db.child("users").child(name).child("name").get().val()
            uid = db.child("users").child(name).child("uid").get().val()
            return {'success':'true', 'name':name, 'uid':uid}

        return {'success':'false'}
        '''with open('userdata.csv', 'r') as user_data:
            rdr = csv.reader(user_data)
            for line in rdr:
                if line[1] == email and line[3] == passw:
                    return {'success':'true','uid':line[2],'name':line[0]}
        return {'result':'fail'}'''

class Register(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        email = args['email']
        passw = args['pass']
        '''exist = False
        length = 0
        with open('userdata.csv', 'r') as user_data:
            rdr = csv.reader(user_data)
            for line in rdr:
                length += 1
                if line[1] == email:
                    exist = True
                    break
        if exist:
            return {'success':'false'}'''
        try:
            auth.create_user_with_email_and_password(email,passw)
        except:
            message="Unable to create account try again"
            return {'success':'false'}

        '''with open('userdata.csv', 'a', newline="") as user_data:
            wr = csv.writer(user_data)
            wr.writerow([name,email,length + 19,passw])'''
        temp_uid = random.randrange(15,200)
        data_t = {"name": name, "pw": passw, "uid": temp_uid}
        db.child("users").child(name).set(data_t)

        return {'success':'true', 'uid':temp_uid, 'name':name}

class SearchBeer(Resource):
    def post(self):
        args = parser.parse_args()
        temp = []
        temp_len = 0
        with open('jsondata.csv') as json_data:
            rdr = csv.reader(json_data)
            for line in rdr:
                if args['name'] in line[0] and line[0] != "name":
                    temp_len += 1
                    temp.append({'bid':line[1], 'name':line[0], 'imagePath':line[6], 'ibu':line[3], 'srm':line[5], 'abv':line[4]})
                if temp_len > 10:
                    break
        return {'beers':temp}

class userRecommandation(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        uid = db.child("users").child(name).child("uid").get().val()
        #print(name)
        #uid = find_uid(email)
        #print(uid)
        rec_list = get_recommendation_list(uid)
        temp = []
        with open('jsondata.csv', 'r') as f:
            rdr = csv.reader(f)
            for line in rdr:
                for i in range(len(rec_list)):
                    if line[1] != "bid":
                    #print(type(line[1]), type(rec_list[i]))
                        if int(line[1]) == rec_list[i]:
                            temp.append({'bid':line[1], 'name':line[0], 'imagePath':line[6], 'ibu':line[3], 'srm':line[5], 'abv':line[4]})
        return jsonify(beers=temp)
        #return {'beers':temp}

class Advertisement(Resource):
    def get(self):
        random_temp = []
        temp = []
        ran_num = random.randint(1,500)
        for i in range(8):
            while ran_num in random_temp:
                ran_num = random.randint(1,500)
            random_temp.append(ran_num)

        with open('jsondata.csv', 'r') as f:
            rdr = csv.reader(f)
            for line in rdr:
                for i in range(8):
                    if line[1] != "bid":
                        if int(line[1]) == random_temp[i]:
                            temp.append({'bid':line[1], 'name':line[0], 'imagePath':line[6], 'ibu':line[3], 'srm':line[5], 'abv':line[4]})
        return {'beers':temp}

class BeerRecommandation(Resource):
    def post(self):
        args = parser.parse_args()
        bid = args['bid']
        temp = []
        temp_num = 0
        group_num = 1
        with open('jsondata.csv', 'r') as f:
            rdr = csv.reader(f)
            for line in rdr:
                if line[1] != "bid":
                    if int(line[1]) == bid:
                        group_num = line[2]
                        break
        with open('jsondata.csv', 'r') as f:
            rdr = csv.reader(f)
            for line in rdr:
                if line[2] == group_num and int(line[1]) != bid:
                    group_num = line[2]
                    temp.append({'bid':line[1], 'name':line[0], 'imagePath':line[6], 'ibu':line[3], 'srm':line[5], 'abv':line[4]})
                    temp_num +=1
                    if temp_num == 8:
                        break
        return {'beers':temp}

class Validation(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        Bid = args['bid']
        Rating = args['rating']
        BeerName = ''
        with open('jsondata.csv', 'r') as f:
            rdr = csv.reader(f)
            for line in rdr:
                if line[1] != "bid":
                    if int(line[1]) == Bid:
                        BeerName = line[0]
                        break
        data_t = {BeerName: int(Rating)}
        try:
            db.child("users").child(name).child("beer").update(data_t)
        except:
                return {'success':'false'}
        return {'success':'true'}


'''
class BeerdataFromBid(Resource):
    def post(self, beer_id):
        args = parser.parse_args()
        with open('data.json') as json_file:
            bid = beer_id - 1
            json_data = json.load(json_file)
            return jsonify(name=json_data[bid]['name'], group=json_data[bid]['group'])
    def post(self):
        beername = "Asahi"
        group = db.child("0").child(beername).child("group").get().val()
        IBU = db.child("0").child(beername).child("IBU").get().val()
        ABV = db.child("0").child(beername).child("ABV").get().val()
        SRM = db.child("0").child(beername).child("SRM").get().val()
        labels_64 = db.child("0").child(beername).child("labels_64").get().val()
        rating = db.child("0").child(beername).child("rating").get().val()
        return {'1':group,'2':IBU,'3':ABV,'4':SRM,'5':labels_64,'6':rating}

    def get(self):
        return {'result': 'getbeer'}
'''

api.add_resource(Register, '/register')
api.add_resource(SearchBeer, '/search')
api.add_resource(MyLogin, '/login')
api.add_resource(Validation, '/validation')
api.add_resource(userRecommandation, '/userRecommandation')
api.add_resource(BeerRecommandation, '/beerRecommandation')
api.add_resource(Advertisement, '/advertisement')

#api.add_resource(BeerdataFromBid, '/beer/<int:beer_id>')
#name = "cndgus1902"
#print(db.child("user").child(name).child("uid").get().val())
#print()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)
