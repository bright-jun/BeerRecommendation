from pyrebase import pyrebase
from operator import eq

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

db = firebase.database()

def make_userdata_by_selected_name(array, selected_user):

    beers = db.child("rated").child(selected_user).get()
    for beer in beers.each():
        bid = db.child("0").child(beer.key()).child("bid").get().val()
        rating = db.child("rated").child(selected_user).child(beer.key()).child("rating").get().val()
        array.append([selected_user, bid, rating])

    all_users = db.child("rated").get()
    for user in all_users.each():
        all_beers = db.child("rated").child(user.key()).get()
        if eq(user.key(), selected_user) == False:
            for beer in all_beers.each():
                bid = db.child("0").child(beer.key()).child("bid").get().val()
                rating = db.child("rated").child(user.key()).child(beer.key()).child("rating").get().val()
                array.append([user.key(), bid, rating])

def make_userdata(array):  # selected_user : user
    all_users = db.child("users").get()
    for user in all_users.each():
        all_beers = db.child("users").child(user.key()).child("beer").get()
        if all_beers.each() != None:
            for beer in all_beers.each():
                uid = db.child("users").child(user.key()).child("uid").get().val()
                bid = db.child("0").child(beer.key()).child("bid").get().val()
                rating = db.child("users").child(user.key()).child("beer").child(beer.key()).get().val()
                #print(bid)
                #print(rating)
                array.append([uid, bid, rating])
