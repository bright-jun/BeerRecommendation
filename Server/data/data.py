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

array = []

def make_userdata(array, selected_user):  # selected_user : user의 이름

    # 해당 유저(selected_user)를 배열의 0행으로 놓는 과정

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


make_userdata(array, "오충현")
print(array)
