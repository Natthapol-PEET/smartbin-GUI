# python -m pip install --user Pyrebase
import pyrebase

config = {
  "apiKey": "AIzaSyDKqw81UDwGDiJJSjHF7uQI-AECzbz9S9w",
  "authDomain": "g0lineapi-opxykx.firebaseapp.com",
  "databaseURL": "https://g0lineapi-opxykx.firebaseio.com",
  "storageBucket": "g0lineapi-opxykx.appspot.com",
  "serviceAccount": "serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# upload
def upload_preds(img_name, ClassFolder):
    ClassFolder = "image predict/" + ClassFolder + '/' + img_name
    storage.child(ClassFolder).put(img_name)

def upload_origin(img_name, ClassFolder):
    ClassFolder = "image origin/" + ClassFolder + '/' + img_name
    storage.child(ClassFolder).put(img_name)

# download
# storage.child("image/new.jpg").download("example.jpg")

# get url image
# url = storage.child("image/new.jpg").get_url(None)
# print(url)

# list all image
# files = storage.list_files()
# for file in files:
#     print(storage.child(file.name).get_url(None))
#     print(file.name)