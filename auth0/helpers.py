
import google_auth_oauthlib.flow
from django.conf import settings
# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.


def get_google_oauth_url():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_OAUTH_CONFIG['client_secret_file'],
        scopes=settings.GOOGLE_OAUTH_CONFIG['scope'],
        redirect_uri=settings.GOOGLE_OAUTH_CONFIG['redirect_uri'])

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    return authorization_url, state


oauth_google_authorization_url, oauth_state = get_google_oauth_url()
