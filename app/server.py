from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.firebase_functions import *
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from uuid_generator import deterministic_uuid_from_email

load_dotenv()
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.readonly"
]


# Initialize FastAPI app
app = FastAPI(title="Placement Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow all origins
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
async def root():
    return {"message": "Placement Tracker API is running!"}


# Add or update a user
@app.post("/api/users/")
async def add_user(user: User):
    f_add_user(**user.model_dump())
    return {"message": f"User {user.uid} added/updated successfully."}


# Get a user by UID
@app.get("/api/users/{uid}")
async def get_user(uid: str):
    user = f_get_user(uid)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User {uid} not found.")


@app.get("/api/branches")
async def get_branches():
    return { "branches" : f_get_branches()}

@app.post("/api/auth/google/callback")
async def google_auth_callback(request: Request):
    data = await request.json()
    print("Raw request data:", data)

    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    print("Auth flow initialized")
    try:
        # Exchange the code for tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Get user info
        user_info_service = build("oauth2", "v2", credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()

        uid = deterministic_uuid_from_email(user_info.get("email"))

        print("User info fetched:", user_info)

        user = f_get_user(uid)
        if user:
            return user
        raise HTTPException(status_code=404, detail=f"User {uid} not found.")

        return JSONResponse({
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "email": user_info.get("email"),
            "name": user_info.get("name"),
        })

    except Exception as e:
        print("Exception occurred in callback:", e)
        raise HTTPException(status_code=500, detail=str(e))