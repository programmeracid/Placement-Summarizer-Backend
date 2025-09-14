import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

def firestore_init():

    # --- Firestore setup (requires service account) ---
    # In backend, you need a service account to actually connect.
    # Download serviceAccountKey.json from Firebase Console > Settings > Service accounts
    # Then load it securely (better: use env vars instead of raw file)

    service_account_path = "placement-tracker-c7d72-ae8bf36ecac6.json"  # keep this in .gitignore

    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db


# Example usage


if __name__ == "__main__":
    print('nob')
