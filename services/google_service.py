from googleapiclient.discovery import build
from auth.google_auth import get_credentials
import os

GOOGLE_FOLDER_ID = os.environ.get("GOOGLE_FOLDER_ID")

def get_google_services():

    creds = get_credentials()

    if not creds:
        raise Exception("Google belum login")

    drive_service = build("drive", "v3", credentials=creds)

    docs_service = build("docs", "v1", credentials=creds)

    return docs_service, drive_service
