import firebase_admin
from firebase_admin import credentials, db
import time

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://hand-gesture-drone-controller-default-rtdb.asia-southeast1.firebasedatabase.app/"})

# Reference to the "instructions" node in the database
ref = db.reference('/')

while True:
    try:
      
      data = ref.get()
      last_key = list(data.keys())[-1]
      last_element = data[last_key]
      instruction_value = last_element.get('instruction', '')
      print(instruction_value)


    except KeyboardInterrupt:
        print("Program terminated by user.")
        break
