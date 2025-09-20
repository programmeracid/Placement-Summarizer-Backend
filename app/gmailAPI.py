from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import requests, os
from dotenv import load_dotenv
import base64
import pandas as pd
from io import BytesIO
from bs4 import BeautifulSoup
import re
import json

from app.email_scraper import extract_email_info
from app.excel_parser import parse_excel
from app.checkMail import strict_check

load_dotenv()

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def get_access_token(refresh_token: str):
    data = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=data)

    print(response)
    if response.status_code == 200:
        tokens = response.json()
        return tokens["access_token"]
    else:
        raise Exception(f"Error refreshing token: {response.text}")

def get_message_details(service, message_id: str):
    msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()

    # Extract headers
    headers = msg["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), None)
    sender = next((h["value"] for h in headers if h["name"] == "From"), None)

    body = ""
    dataframes = []  # store DataFrames from excel attachments

    def clean_text(text: str) -> str:
        """
        Clean extracted email text by removing extra whitespace,
        newlines, and non-breaking spaces.
        """
        # Replace non-breaking space with normal space
        text = text.replace("\xa0", " ")
        # Remove newlines, tabs, and collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        #text = text[:-1231] #stripping samuel rajakumar's bs
        
        return text.strip()

    def parse_parts(parts):
        nonlocal body, dataframes
        for part in parts:
            mime_type = part.get("mimeType")
            body_data = part.get("body", {}).get("data")
            attachment_id = part.get("body", {}).get("attachmentId")

            if body_data:
                decoded = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
                if mime_type == "text/plain":
                    body += decoded + " "
                elif mime_type == "text/html":
                    # Convert HTML → plain text
                    soup = BeautifulSoup(decoded, "html.parser")
                    body += soup.get_text(separator=" ").strip() + " "

            elif attachment_id:
                # Fetch attachment bytes
                att = service.users().messages().attachments().get(
                    userId="me", messageId=msg["id"], id=attachment_id
                ).execute()
                file_data = base64.urlsafe_b64decode(att["data"])
                filename = part.get("filename", "")

                # If it's an Excel sheet, read directly into pandas
                if filename.endswith((".xlsx", ".xls")):
                    df = pd.read_excel(BytesIO(file_data), header=None)
                    dataframes.append({"filename": filename, "dataframe": df})

            if "parts" in part:
                parse_parts(part["parts"])

    # Parse payload
    if "parts" in msg["payload"]:
        parse_parts(msg["payload"]["parts"])
    else:
        body_data = msg["payload"]["body"].get("data")
        if body_data:
            decoded = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
            soup = BeautifulSoup(decoded, "html.parser")
            body = soup.get_text(separator=" ")

    # Clean final body text
    body = clean_text(body)

    return {
        "subject": clean_text(subject) if subject else None,
        "from": clean_text(sender) if sender else None,
        "body": body,
        "excel_attachments": dataframes,  # list of {"filename": str, "dataframe": pd.DataFrame}
    }

def is_placement_email(details):
    if "Helpdesk CDC" in details["from"] or "VITCC Placement" in details["from"]:
        return strict_check(details)
    else:
        return strict_check(details)

def read_user_emails(access_token: str):
    creds = Credentials(token=access_token)
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", maxResults=5).execute()
    messages = results.get("messages", [])

    email_details = []
    for m in messages:
        details = get_message_details(service, m["id"])
        if not is_placement_email(details):
            print(f"\n!!!\nEmail with subject:\n<{details['subject']}> rejected\nSender:\n{details['from']}")
            continue
        print(f"\nEmail with subject:\n<{details['subject']}> accepted\nSender:\n{details['from']}")
        email_details.append(details)

    return email_details

def parse_email(email: dict):
    body = email["body"]
    attachments = email["excel_attachments"]
    email_info = extract_email_info(body)
    email_info = email_info.strip('\\njson` ')
    email_info = json.loads(email_info.replace("\n",""))
    # print(email_info.keys())
    for i in email_info:
        if str(email_info[i]).strip()=="False":
            email_info[i]=False
    shortlists = []
    for i in attachments:
        shortlists.append(parse_excel(i['dataframe']))
    email_info["shortlists"]=shortlists
    return email_info


def parse_pubsub_message(pubsub_message):
    data = pubsub_message["message"]["data"]
    decoded = base64.b64decode(data).decode("utf-8")
    return json.loads(decoded)

def fetch_new_messages(service, start_history_id):
    history = service.users().history().list(
        userId="me",
        startHistoryId=start_history_id,
        historyTypes=["messageAdded"]
    ).execute()

    messages = []
    if "history" in history:
        for record in history["history"]:
            if "messagesAdded" in record:
                for m in record["messagesAdded"]:
                    messages.append(m["message"]["id"])  # ✅ THIS is the Gmail message.id
    return messages[0]


def read_latest_mail(access_token, message):
    creds = Credentials(token=access_token)
    service = build("gmail", "v1", credentials=creds)
    message = parse_pubsub_message(message)
    message_id = fetch_new_messages(service, message['historyId'])
    details = get_message_details(service, message_id)
    if not is_placement_email(details):
        print(f"\n!!!\nEmail with subject:\n<{details['subject']}> rejected\nSender:\n{details['from']}")
            
    print(f"\nEmail with subject:\n<{details['subject']}> accepted\nSender:\n{details['from']}")
    email = parse_email(details)
    return email

if __name__ == "__main__":
    refresh_token = ""
    access_token = get_access_token(refresh_token)
    emails = read_user_emails(access_token)
    # print(*emails, sep = '\n')
    # print(emails[0])
    for email in emails:
        print(parse_email(email)) 