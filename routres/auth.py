from flask import redirect, session, url_for, request

from auth.google_auth import create_flow, save_credentials

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():

    flow = create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent"
    )

    session["state"] = state

    return redirect(authorization_url)


@auth_bp.route("/oauth2callback")
def oauth2callback():

    flow = create_flow()

    flow.fetch_token(authorization_response=request.url)

    save_credentials(flow.credentials)

    return redirect(url_for("dashboard"))
