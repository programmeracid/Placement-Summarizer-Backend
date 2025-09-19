import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import os, dotenv
import json

# Load environment variables
load_dotenv()

def firestore_init():



    # --- Firestore setup (requires service account) ---
    # In backend, you need a service account to actually connect.
    # Download serviceAccountKey.json from Firebase Console > Settings > Service accounts
    # Then load it securely (better: use env vars instead of raw file)

    firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

    if not firebase_json:
        firebase_cred = "placement-tracker-c7d72-ae8bf36ecac6.json"  # keep this in .gitignore
    else:
        firebase_cred = json.loads(firebase_json)
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_cred)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db


# Example usage


if __name__ == "__main__":
    firestore_init()
