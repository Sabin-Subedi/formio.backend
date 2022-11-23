import google.oauth2.credentials
import google_auth_oauthlib.flow
from django.contrib.sessions.backends.db import SessionStore

# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.


def get_google_oauth_url():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'])

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = 'http://localhost:8000/auth/oauth/google/redirect/'

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # # Store the state so the callback can verify the auth server response.
    # flask.session['state'] = state

    return authorization_url, state,flow


oauth_google_authorization_url, oauth_state,flow = get_google_oauth_url()
