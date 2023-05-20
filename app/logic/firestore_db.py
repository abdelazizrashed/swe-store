
import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("app/logic/service-account-key.json")
fb_app = firebase_admin.initialize_app(cred, {
    "storageBucket": "swe-store.appspot.com"
})
db = firestore.client()

bucket = storage.bucket()
