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

# Mengambil REDIRECT_URI dari env (Pastikan di Render diisi URL prod, di lokal diisi 127.0.0.1)
REDIRECT_URI = os.environ.get(
    "OAUTH_REDIRECT_URI", "http://127.0.0.1:5000/oauth2callback"
)


def get_client_secrets_path():
    """Fungsi otomatis untuk mendeteksi lokasi file credentials.json"""
    # 1. Cek jalur standar Secret File dari Render
    render_secrets_path = "/etc/secrets/credentials.json"
    if os.path.exists(render_secrets_path):
        return render_secrets_path

    # 2. Cek di root folder (bisa di Render runtime atau di komputer lokal Anda)
    local_root_path = "credentials.json"
    if os.path.exists(local_root_path):
        return local_root_path

    raise FileNotFoundError(
        "File credentials.json tidak ditemukan di lokal maupun di /etc/secrets/"
    )


def create_flow():
    # Menentukan path file secara dinamis dan otomatis
    client_secrets_file = get_client_secrets_path()

    if not REDIRECT_URI:
        raise ValueError("Environment variable OAUTH_REDIRECT_URI belum dikonfigurasi!")

    return Flow.from_client_secrets_file(
        client_secrets_file, scopes=SCOPES, redirect_uri=REDIRECT_URI
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
