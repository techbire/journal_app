import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase
def initialize_firebase():
    with open('firebase_config.json') as f:
        config = json.load(f)
    
    cred = credentials.Certificate(config)
    firebase_admin.initialize_app(cred)

# Add transcription to Firestore
def save_transcription(transcription_text):
    db = firestore.client()
    doc_ref = db.collection(u'transcriptions').document()
    doc_ref.set({
        u'transcription': transcription_text,
        u'timestamp': firestore.SERVER_TIMESTAMP
    })
    print("Transcription saved to Firestore")
