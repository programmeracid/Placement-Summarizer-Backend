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
<<<<<<< Updated upstream
=======
from app.uuid_generator import deterministic_uuid_from_email
>>>>>>> Stashed changes

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
    email: str
    firstName: str
    lastName: str
    branch: str
    regNo: str
    passingYear: int
    cgpa: float
    marks10th: float
    marks12th: float
    uid: str
    placementDriveInfo: Optional[str] = ''

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
    f_add_user(
        uid=user.uid,
        email=user.email,
        first_name=user.firstName,
        last_name=user.lastName,
        reg_no=user.regNo,
        cgpa=user.cgpa,
        branch=user.branch,
        passing_year=user.passingYear,
        marks_10th=user.marks10th,
        marks_12th=user.marks12th,
        placement_drive_info=user.placementDriveInfo
    )
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

<<<<<<< Updated upstream
        print("User info fetched:", user_info)

        return JSONResponse({
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "email": user_info.get("email"),
            "name": user_info.get("name"),
        })
=======
        uid = str(deterministic_uuid_from_email(user_info.get("email")))

        print("User info fetched:", user_info)

        if f_get_user(uid): return JSONResponse(status_code = 200, content={'uid':uid})
        else: return JSONResponse(status_code = 404, content={'uid':uid})
>>>>>>> Stashed changes

    except Exception as e:
        print("Exception occurred in callback:", e)
        raise HTTPException(status_code=500, detail=str(e))