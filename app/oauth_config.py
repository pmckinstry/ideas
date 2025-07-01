import requests
from urllib.parse import urlencode
from flask import current_app

# Google OAuth Configuration
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid_configuration"

def get_google_client_id():
    """Get Google client ID from app config"""
    return current_app.config.get('GOOGLE_CLIENT_ID', '')

def get_google_client_secret():
    """Get Google client secret from app config"""
    return current_app.config.get('GOOGLE_CLIENT_SECRET', '')

# OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def get_google_auth_url(redirect_uri, state=None):
    """Generate Google OAuth authorization URL"""
    params = {
        'client_id': get_google_client_id(),
        'redirect_uri': redirect_uri,
        'scope': 'openid email profile',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    if state:
        params['state'] = state
    
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

def get_google_token(code, redirect_uri):
    """Exchange authorization code for access token"""
    data = {
        'client_id': get_google_client_id(),
        'client_secret': get_google_client_secret(),
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get token: {response.text}")

def get_google_user_info(access_token):
    """Get user information from Google"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get user info: {response.text}")

def is_google_oauth_enabled():
    """Check if Google OAuth is properly configured"""
    return bool(get_google_client_id() and get_google_client_secret()) 