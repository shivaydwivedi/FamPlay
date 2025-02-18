from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, get


BASE_URL = "https://api.spotify.com/v1/me/"


def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        print(f"Tokens found for session: {session_id}")
        return user_tokens[0]
    else:
        print(f"No tokens found for session: {session_id}")
        return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                                   'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            print("Tokens expired. Refreshing...")
            refresh_spotify_token(session_id)
        else:
            print("Tokens are valid.")
        return True

    print("No tokens available. User is not authenticated.")
    return False


def refresh_spotify_token(session_id):
    tokens = get_user_tokens(session_id)
    if not tokens or not tokens.refresh_token:
        print(f"No refresh token found for session: {session_id}")
        return

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': tokens.refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })

    if response.status_code != 200:
        print(f"Failed to refresh token: {response.json()}")
        return

    response_data = response.json()
    access_token = response_data.get('access_token')
    token_type = response_data.get('token_type')
    expires_in = response_data.get('expires_in')
    refresh_token = response_data.get('refresh_token', tokens.refresh_token)  # Keep old refresh token if not returned

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)
