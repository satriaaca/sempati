from flask import Flask, session, redirect, url_for, request, render_template, jsonify
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

from services.lapinhar_service import create_lapinhar_document
from services.google_service import get_google_services, GOOGLE_FOLDER_ID
from auth.google_auth import create_flow, save_credentials, get_credentials, REDIRECT_URI

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")


if os.getenv("FLASK_ENV") != "production":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

# CLIENT_SECRETS_FILE = "credentials.json"

# REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:5000/oauth2callback")


# def create_flow():
#     return Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE,
#         scopes=SCOPES,
#         redirect_uri=REDIRECT_URI,
#     )


# def save_credentials(credentials):
#     session["credentials"] = {
#         "token": credentials.token,
#         "refresh_token": credentials.refresh_token,
#         "token_uri": credentials.token_uri,
#         "client_id": credentials.client_id,
#         "client_secret": credentials.client_secret,
#         "scopes": credentials.scopes,
#     }


# def get_credentials():
#     if "credentials" not in session:
#         return None

#     return Credentials(**session["credentials"])


PUBLIC_ENDPOINTS = {
    "login",
    "oauth2callback",
    "logout",
    "static",
}


@app.before_request
def require_google_login():

    endpoint = request.endpoint

    # print("REQUEST:", request.path)
    # print("ENDPOINT:", endpoint)
    # print("SESSION:", session.keys())

    if endpoint in PUBLIC_ENDPOINTS:
        return

    if "credentials" not in session:

        session["next_url"] = request.url

        return redirect(url_for("login"))


@app.route("/login")
def login():
    flow = create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )

    session["state"] = state
    session["code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():

    flow = create_flow()

    flow.code_verifier = session["code_verifier"]

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    save_credentials(credentials)

    print("LOGIN BERHASIL")
    print(session)

    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/input/lapinhar")
def lapinhar_page():
    return render_template("lapinhar.html")


@app.route("/api/save-form", methods=["POST"])
def save_form():

    try:

        data = request.get_json()

        docs_service, drive_service = get_google_services()

        url = create_lapinhar_document(
            drive_service=drive_service,
            form_data=data,
            target_folder_id=GOOGLE_FOLDER_ID,
        )

        return jsonify({"message": "Dokumen berhasil dibuat", "url": url})

    except Exception as e:

        return jsonify({"error": str(e)}), 500


@app.route("/preview/lapinhar")
def preview_lapinhar():

    return render_template("preview_lapinhar.html")


if __name__ == "__main__":
    app.run(debug=True)
