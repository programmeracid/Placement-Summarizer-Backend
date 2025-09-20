from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.firebase_functions import *
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os, requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.uuid_generator import deterministic_uuid_from_email

load_dotenv()
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
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
    
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    try:
        client_config = {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": REDIRECT_URI,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }

        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        print(data)
        print(flow)
        flow.fetch_token(code=code)

        credentials = flow.credentials
        print(credentials)

        user_info_service = build("oauth2", "v2", credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        print(user_info)
        email = user_info.get("email")
        url = f"https://gmail.googleapis.com/gmail/v1/users/{email}/watch"
        data = {
        "labelIds": [
            "INBOX"
        ],
        "topicName": "projects/placement-tracker-471904/topics/read-emails"
        }
        
        access_token = credentials.token   # from your Google OAuth flow
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=headers)

        print("Status:", response.status_code)
        print("Response JSON:", response.json())

        uid = str(deterministic_uuid_from_email(email))

        if credentials.refresh_token:
            save_refresh_token(uid, credentials.refresh_token)

        return JSONResponse({
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "email": user_info.get("email"),
            "name": user_info.get("name"),
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google auth failed: {str(e)}")


    except Exception as e:
        print("Exception occurred in callback:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/push-notification")
async def get_post_notification(request: Request):
    data = await request.json()
    print(data)
    return {"message": f"got smth"}