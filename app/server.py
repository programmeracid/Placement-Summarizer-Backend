from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.firebase_functions import *
import requests
from dotenv import load_dotenv

load_dotenv()
import os


# Initialize FastAPI app
app = FastAPI(title="Placement Tracker API")

origins = ["http://localhost:3000",
           "http://27.5.78.173:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow specific origins
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # allow all headers
)

# Example data model
class User(BaseModel):
    uid: str
    email: str
    first_name: str
    last_name: str
    reg_no: str
    cgpa: float
    branch: str
    passing_year: int
    marks_10th: float
    marks_12th: float
    placement_drive_info: str

class GoogleUser(BaseModel):
    uid: str
    name: str
    email: str
    access_token: str




# Root route
@app.get("/")
def root():
    return {"message": "Placement Tracker API is running!"}


# Add or update a user
@app.post("/api/users/")
def add_user(user: User):
    f_add_user(**user.model_dump())
    return {"message": f"User {user.uid} added/updated successfully."}


# Get a user by UID
@app.get("/api/users/{uid}")
def get_user(uid: str):
    user = f_get_user(uid)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User {uid} not found.")




@app.get("/api/branches")
def get_branches():
    return { "branches" : f_get_branches()}

@app.post("/api/auth/google")
def get_google_auth(googleUser: GoogleUser):
    

    print(googleUser)

    # TODO: validate Firebase accessToken if needed
    # TODO: save user data into Firestore/DB

    return {
        "message": "User data received successfully",
        "uid": googleUser.uid,
        "name": googleUser.name,
        "email": googleUser.email
    }

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

@app.get("/api/auth/callback")
def auth_callback(request: Request, code: str):
    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code"
    }

    r = requests.post(GOOGLE_TOKEN_URL, data=data)
    tokens = r.json()
    print(tokens)

    # tokens contains access_token + refresh_token
    # Save refresh_token in your DB for that user
    return tokens