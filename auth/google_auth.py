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

# Mengambil string JSON dan Redirect URI langsung dari Environment Variable
CLIENT_SECRET_ENV = os.environ.get("GOOGLE_CREDENTIALS")
REDIRECT_URI = os.environ.get(
    "OAUTH_REDIRECT_URI", "http://127.0.0.1:5000/oauth2callback"
)


def create_flow():
    if not CLIENT_SECRET_ENV:
        raise ValueError("Environment variable GOOGLE_CREDENTIALS belum di-set!")
    if not REDIRECT_URI:
        raise ValueError("Environment variable OAUTH_REDIRECT_URI belum di-set!")

    # Mengubah string JSON dari Env Var menjadi dictionary Python
    client_config = json.loads(CLIENT_SECRET_ENV)

    # Menggunakan dari_client_config agar tidak membutuhkan file credentials.json fisik
    return Flow.from_client_config(
        client_config, scopes=SCOPES, redirect_uri=REDIRECT_URI
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
