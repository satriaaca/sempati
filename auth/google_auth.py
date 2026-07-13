import json
import os
from flask import session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

# Mengambil string JSON dan Redirect URI dari Environment Variable
CLIENT_SECRET_ENV = os.environ.get("GOOGLE_CREDENTIALS")
REDIRECT_URI = os.environ.get(
    "OAUTH_REDIRECT_URI", "http://127.0.0.1:5000/oauth2callback"
)

# Nama file fallback jika environment variable kosong
CREDENTIALS_FILE = "credentials.json"


def create_flow():
    if not REDIRECT_URI:
        raise ValueError("Environment variable OAUTH_REDIRECT_URI belum di-set!")

    # Jalur 1: Jika Environment Variable tersedia, gunakan dari_client_config
    if CLIENT_SECRET_ENV:
        try:
            client_config = json.loads(CLIENT_SECRET_ENV)
            return Flow.from_client_config(
                client_config, scopes=SCOPES, redirect_uri=REDIRECT_URI
            )
        except json.JSONDecodeError:
            raise ValueError("Format JSON pada GOOGLE_CREDENTIALS tidak valid!")

    # Jalur 2: Jika Env Var kosong, cari file credentials.json fisik
    elif os.path.exists(CREDENTIALS_FILE):
        return Flow.from_client_secrets_file(
            CREDENTIALS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
        )

    # Jalur 3: Kedua opsi tidak tersedia, lemparkan error
    else:
        raise FileNotFoundError(
            f"Konfigurasi tidak ditemukan! Environment variable GOOGLE_CREDENTIALS "
            f"kosong dan file '{CREDENTIALS_FILE}' tidak ditemukan di direktori project."
        )


def save_credentials(credentials):
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def get_credentials():
    if "credentials" not in session:
        return None

    return Credentials(**session["credentials"])