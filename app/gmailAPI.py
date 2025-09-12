from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_message_details(service, message_id: str):
    msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()

    # Extract headers
    headers = msg["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), None)
    sender = next((h["value"] for h in headers if h["name"] == "From"), None)
    snippet = msg.get("snippet", "")

    return {
        #"id": msg["id"],
        #"threadId": msg["threadId"],
        "subject": subject,
        "from": sender,
        #"snippet": snippet
    }


def read_user_emails(access_token: str):
    creds = Credentials(token=access_token)
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", maxResults=5).execute()
    messages = results.get("messages", [])

    email_details = []
    for m in messages:
        details = get_message_details(service, m["id"])
        email_details.append(details)

    return email_details


