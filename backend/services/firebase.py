import firebase_admin
from firebase_admin import credentials, firestore

# We use a variable to store the app so it's a singleton
app = None

def get_db():
    global app
    # Only initialize if it hasn't been initialized yet
    if not firebase_admin._apps:
        cred = credentials.Certificate("backend/serviceAccountKey.json")
        app = firebase_admin.initialize_app(cred)
    
    return firestore.client()

# Create the db instance once
db = get_db()
