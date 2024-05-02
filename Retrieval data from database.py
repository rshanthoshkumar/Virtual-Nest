# import required modules
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

try:

    cred = credentials.Certificate(r"#json file")

    firebase_admin.initialize_app(cred, {
        'databaseURL': '#firebase URL'
    })

    ref = db.reference("/")


    print(ref.get())
except Exception as e:
    print("The error is: ", e)
